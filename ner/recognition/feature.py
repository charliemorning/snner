
from ner.recognition.data import xml2bio


def get_word_and_cate(text, **kwargs):

    # to tokenize the piece
    try:
        bioList = xml2bio(text, **kwargs)
    except:
        print 'format error'
        raise

    wordCatePairList = [bio for bio in bioList]

    wordV = [bio[0] for bio in wordCatePairList]

    cateV = [bio[1] for bio in wordCatePairList]

    return wordV, cateV




def make_feature_vectors(text, **kwargs):
    """
    an annotated weibo piece was passed as a 1 dimension vector.
    the output was the matrix whose row was the current token and its one dimension feature vector.
    """

    # first element is the token itself
    #isFirstNameV = __make_feature_vector(bioList, create_is_first_name_feature)

    # first element is the token itself
    #isLocationV = __make_feature_vector(bioList, create_is_chinese_gazetteer_feature)

    # the last element is the category

    return get_word_and_cate(text, **kwargs)


def to_feature_vector_with_cate(text, **kwargs):
    """
    """

    wordV, cateV = make_feature_vectors(text, **kwargs)
    return zip(wordV, cateV)


def stringify_feature_vecter_with_cate(f):

    s = str()
    for i in f:
        s += i + '\t'
    return s[:-1]


def create_sns_tags(data, cates):



    for i in xrange(len(data)):
        l = []
        l.append(data[i], cates[i])


    pass


def create_tags(data, **kwargs):

    fm = to_feature_vector_with_cate(data, **kwargs)

    tags = []

    for fv in fm:
        s = stringify_feature_vecter_with_cate(fv)

        tags.append(s)

    return tags





