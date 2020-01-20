import gensim
import nltk

import textwrap
import datetime
import inspect
import re
import enlighten
import numpy as np
import warnings


from pathlib import Path

from autogoal.grammar import Discrete, Continuous, Categorical, Boolean

languages = ["arabic",\
             "danish",\
             "dutch",\
             "english",\
             "finnish",\
             "french",\
             "german",\
             "hungarian",\
             "italian",\
             "norwegian",\
             "portuguese",\
             "romanian",\
             "russian",\
             "spanish",\
             "swedish"]

languages_re = re.compile("|".join(languages))

def build_nltk_wrappers():
    imports = _walk(nltk)
    imports += _walk(nltk.cluster)
    imports += _walk(gensim.models)
    
    manager = enlighten.get_manager()
    counter = manager.counter(total=len(imports), unit="classes")

    with open(Path(__file__).parent / "_generated.py", "w") as fp:
        fp.write(textwrap.dedent(
            f"""
            # AUTOGENERATED ON {datetime.datetime.now()}
            ## DO NOT MODIFY THIS FILE MANUALLY

            from autogoal.grammar import Continuous, Discrete, Categorical, Boolean
            from autogoal.kb._data import *
            from numpy import inf, nan
            """
        ))
        
        for cls in imports:
            counter.update()
            _write_class(cls, fp)

    counter.close()
    manager.stop()


def _write_class(cls, fp):
    try:
        args = _get_args(cls)
    except Exception as e:
        warnings.warn("Error to generate wrapper for %s : %s" %(cls.__name__, e))
        return

    s = " " * 4
    args_str = f",\n{s * 4}".join(f"{key}: {value}" for key, value in args.items())
    self_str = f"\n{s * 4}".join(f"self.{key}={key}" for key in args)
    init_str = f",\n{s * 5}".join(f"{key}={key}" for key in args)
    
    print(cls)
    class_code = f"""
        from {cls.__module__} import {cls.__name__} as _{cls.__name__}

        class {cls.__name__}(_{cls.__name__}):
            def __init__(
                self,
                {args_str}
            ):
                {self_str}

                super().__init__(
                    {init_str}
                )
            
            def fit_transform(
                self, 
                X, 
                y=None
            ):
                self.fit(X, y=None)
                return self.transform(X)
            
            def fit(
                self, 
                X, 
                y=None
            ):
                pass    
        """
        
    if _is_stemmer(cls): #generate stemmer
        class_code += _write_stemmer(cls)
        
    if _is_lemmatizer(cls): #generate lemmatizer
        class_code += _write_lemmatizer(cls)
        
    if _is_word_tokenizer(cls): #generate word tokenizer
        class_code += _write_word_tokenizer(cls)
        
    if _is_sent_tokenizer(cls): #generate sentence tokenizer
        class_code += _write_sent_tokenizer(cls)
        
    if _is_clusterer(cls): #generate clusterer
        class_code += _write_clusterer(cls)
        
    if _is_word_embbeder(cls): #generate word embbeder
        class_code += _write_word_embbeder(cls)
        print("set as word embbeding algorithm")
        
    if _is_doc_embbeder(cls): #generate document embbeder
        class_code += _write_doc_embbeder(cls)
        print("set as doc embedding algorithm")
    

    fp.write(textwrap.dedent(class_code))
    fp.flush()


def _write_stemmer(cls):
    return """
            def dstem(
                self,
                document
            ):
                return [self.stem(word) for word in document]

            def transform(
                self, 
                X,
                y=None
            ):
                return [self.dstem(x) for x in X]

            def run(self, input: Word(domain='general', language='english')) -> Stem():
                \"\"\"This methods recive a word and transform this in a stem. 
                \"\"\"
                return self.stem(input)
        """
        
def _write_lemmatizer(cls):
    return """
            def dlemmatize(
                self,
                document
            ):
                return [self.lemmatize(word) for word in document]

            def transform(
                self, 
                X,
                y=None
            ):
                return [self.dlemmatize(x) for x in X]

            def run(self, input: Word(domain='general', language='english')) -> Stem():
                \"\"\"This methods recive a word and transform this in a stem. 
                \"\"\"
                return self.lemmatize(input)
        """

def _write_word_tokenizer(cls):
    return """
            def transform(
                self, 
                X,
                y=None
            ):
                return [self.tokenize(x) for x in X]

            def run(self, input: Sentence(domain='general')) -> List(Word()):
                \"\"\"This methods recive a sentece and transform this in a list of tokens (words). 
                \"\"\"
                return self.tokenize(input)
        """
        
def _write_sent_tokenizer(cls):
    return """
            def transform(
                self, 
                X,
                y=None
            ):
                return [self.tokenize(x) for x in X]

            def run(self, input: Document(domain='general')) -> List(Sentence()):
                \"\"\"This methods recive a document and transform this in a list of sentences. 
                \"\"\"
                return self.tokenize(input)
        """

def _write_clusterer(cls):
    return """
            def fit(
                self, 
                X,
                y = None
            ):
                return self.cluster(X)
            
            def predict(
                self,
                x 
            ):
                return self.classify(x)

            #def run(self, input: Document(domain='general')) -> List(Sentence()):
            #    \"\"\"This methods recive a document and transform this in a list of sentences. 
            #    \"\"\"
            #    return self.tokenize(input)"""

def _write_classifier(cls):
    return """
            def fit(
                self, 
                X,
                y
            ):
                return self.train(list(zip(X, y)))
            
            def predict(
                self,
                x  
            ):
                return self.classify(x)

            #def run(self, input: Document(domain='general')) -> List(Sentence()):
            #    \"\"\"This methods recive a document and transform this in a list of sentences. 
            #    \"\"\"
            #    return self.tokenize(input)"""

def _write_doc_embbeder(cls):
    return """
            def fit(
                self, 
                X,
                y
            ):
                #Data must be turned to tagged data as TaggedDocument(List(Token), Tag)
                #Tag use to be an unique integer
                
                from gensim.models.doc2vec import TaggedDocument as _TaggedDocument
                tagged_data = [_TaggedDocument(X[i], str(i)) for i in range(len(X))]
                
                self.build_vocab(tagged_data)
                return self.train(tagged_data, total_examples=model.corpus_count, epochs=model.iter)
                
            
            def transform(
                self,
                X,
                y=None  
            ):
                return [self.infer_vector(x) for x in X]

            #def run(self, input: Document(domain='general')) -> List(Sentence()):
            #    \"\"\"This methods recive a document and transform this in a list of sentences. 
            #    \"\"\"
            #    return self.tokenize(input)"""
            
def _write_word_embbeder(cls):
    return """
            def fit(
                self, 
                X,
                y
            ):  
                self.build_vocab(X)
                return self.train(X, total_examples=model.corpus_count, epochs=model.iter)
                
            
            def transform(
                self,
                X,
                y=None  
            ):
                #Returns 3d matrix for a document list as every word will turn into a vector
                #This will break when indexing a word that is not in the vocabulary trained
                
                return [[self.wv[word] for word in document] for document in X]

            #def run(self, input: Word(domain='general')) -> List(Float()):
            #    \"\"\"This methods recive a word and transform this in a List of floats. 
            #    \"\"\"
            #    return self.tokenize(input)"""


def _is_algorithm(cls, verbose = False):
    return  _is_stemmer(cls, verbose) or\
            _is_lemmatizer(cls, verbose) or\
            _is_word_tokenizer(cls, verbose) or\
            _is_sent_tokenizer(cls, verbose) or\
            _is_clusterer(cls, verbose) or\
            _is_classifier(cls, verbose) or\
            _is_word_embbeder(cls, verbose) or\
            _is_doc_embbeder(cls, verbose)

def _is_stemmer(cls, verbose=False):
    if hasattr(cls, "stem"):
        return True
    return False

def _is_lemmatizer(cls, verbose=False):
    if hasattr(cls, "lemmatize"):
        return True
    return False

def _is_word_tokenizer(cls, verbose=False):
    if not _is_sent_tokenizer(cls) and (hasattr(cls, "tokenize") or hasattr(cls, "word_tokenize")):
        return True
    return False

def _is_sent_tokenizer(cls, verbose=False):
    if "sentence" in str.lower(cls.__name__) or hasattr(cls, "sent_tokenize"):
            return True
    return False

def _is_clusterer(cls, verbose=False):
    if (hasattr(cls, "classify") and hasattr(cls, "cluster")):
        return True
    return False

def _is_classifier(cls, verbose = False):
    if (hasattr(cls, "classify") and hasattr(cls, "train")):
        return True
    return False

def _is_word_embbeder(cls, verbose = False):
    if (hasattr(cls, "build_vocab") and hasattr(cls, "train") and hasattr(cls, "wv")):
        return True
    return False

def _is_doc_embbeder(cls, verbose = False):
    if (hasattr(cls, "build_vocab") and hasattr(cls, "train") and hasattr(cls, "infer_vector")):
        return True
    return False


def _walk(module, name="nltk"):
    imports = []

    def _walk_p(module, name="nltk"):
        all_elements = dir(module)
        for elem in all_elements:

            if elem == "exceptions":
                continue

            name = name + "." + elem

            try:
                obj = getattr(module, elem)

                if isinstance(obj, type):
                    #ignore nltk interfaces
                    if name.endswith("I"):
                        continue

                    if not _is_algorithm(obj):
                        continue
                    
                    imports.append(obj)

                # _walk_p(obj, name) If not module do not walk in it
            except Exception as e:
                pass

            try:
                inner_module = importlib.import_module(name)
                _walk_p(inner_module, name)
            except:
                pass

    _walk_p(module, name)

    imports.sort(key=lambda c: (c.__module__, c.__name__))
    return imports

def _find_parameter_values(parameter, cls):
    documentation = []
    lines = cls.__doc__.split("\n")

    while lines:
        l = lines.pop(0)
        if l.strip().startswith(parameter):
            documentation.append(l)
            tabs = l.index(parameter)
            break

    while lines:
        l = lines.pop(0)

        if not l.strip():
            continue

        if l.startswith(" " * (tabs + 1)):
            documentation.append(l)
        else:
            break

    options = set(re.findall(r"'(\w+)'", " ".join(documentation)))
    valid = []
    invalid = []
    skip = set(["deprecated", "auto_deprecated", "precomputed"])

    for opt in options:
        opt = opt.lower()
        if opt in skip:
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                cls(**{parameter: opt}).fit(np.ones((10, 10)), [True] * 5 + [False] * 5)
                valid.append(opt)
        except Exception as e:
            invalid.append(opt)

    return sorted(valid)

def _find_language_values(cls):
    global languages_re
    documentation = cls.__doc__
    
    return languages_re.findall(str.lower(documentation))

def _get_args(cls):
    full_specs = inspect.getfullargspec(cls.__init__)

    args = full_specs.args
    specs = full_specs.defaults
    
    if 'dm' in args:
        print('a')

    if not args or not specs:
        return {}

    non_kwargs = [arg for arg in args[:-len(specs):] if arg != "self"]
    
    args = args[-len(specs) :]

    args_map = {k: v for k, v in zip(args, specs)}

    

    drop_args = [
        "url",
        "n_jobs",
        "max_iter",
        "class_weight",
        "warm_start",
        "copy_X",
        "copy_x",
        "copy",
        "eps",
        "ignore_stopwords"
    ]

    for arg in drop_args:
        args_map.pop(arg, None)

    result = {}

    for arg, value in args_map.items():
        values = _get_arg_values(arg, value, cls)
        if not values:
            continue
        result[arg] = values
        
    for arg in non_kwargs:
        #special handling of language
        if str.lower(arg) == "language": 
            values = _find_language_values(cls)
            if values:
                result[arg] = Categorical(*values)
                continue
        raise Exception("No values found for positional argument %s " %(arg))
    return result

def _get_arg_values(arg, value, cls):
    if isinstance(value, bool):
        return Boolean()
    if isinstance(value, int):
        return Discrete(*_get_integer_values(arg, value, cls))
    if isinstance(value, float):
        return Continuous(*_get_float_values(arg, value, cls))
    if isinstance(value, str):
        values = _find_parameter_values(arg, cls)
        return Categorical(*values) if values else None
    return None

def _get_integer_values(arg, value, cls):
    if value == 0:
        min_val = -100
        max_val = 100
    else:
        min_val = value // 2
        max_val = 2 * value

    return min_val, max_val

def _get_float_values(arg, value, cls):
    if value == 0:
        min_val = -1
        max_val = 1
    elif 0 < value <= 0.1:
        min_val = value / 100
        max_val = 1
    elif 0 < value <= 1:
        min_val = 1e-6
        max_val = 1
    else:
        min_val = value / 2
        max_val = 2 * value

    return min_val, max_val


if __name__ == "__main__":
    build_nltk_wrappers()
