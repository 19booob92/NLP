# coding=utf-8
import os
import gensim
import numpy as np
from main import XmlParser


def get_topics_doc(question, data_path, n_words=40, n_topics=10):
    question = question.decode('utf-8')
    xml = XmlParser()
    load_dict_path = os.path.join(data_path, "dictionary.dict")
    load_model_path = os.path.join(data_path, "model.lda")
    tokenized_list = xml.filter_article(question)
    dictionary = gensim.corpora.Dictionary.load(load_dict_path)
    lda = gensim.models.ldamodel.LdaModel.load(load_model_path)
    ques_vec = dictionary.doc2bow(tokenized_list)
    topic_vec = np.array(lda[ques_vec])

    idx = np.argsort(-topic_vec[:, 1])
    word_count_array = topic_vec[idx]
    final = []
    for topic in word_count_array:
        final.append(lda.show_topic(topic[0], n_words))
    # find in word keywords
    act_final = []
    for topic in final:
        act_keyword = []
        for f_word, proba in topic:
            if f_word in tokenized_list:
                act_keyword.append(f_word)
        act_final.append(act_keyword)
    return act_final[:n_topics], final[:n_topics]

if __name__ == '__main__':
    new_doc = 'Termin chemia organiczna oznaczał pierwotnie dział chemii zajmujący się systematyką oraz ' \
              'badaniem własności związków organicznych, które, jak wierzono, nie mogą być otrzymane na drodze' \
              ' syntezy laboratoryjnej, a jedynie przez żywe organizmy.Później okazało się jednak, że niemal ' \
              'wszystkie związki chemiczne produkowane przez organizmy żywe da się też sztucznie zsyntezować. ' \
              'Udało się następnie otrzymać wiele związków, które w naturze nie występują, ale których własności ' \
              'są zbliżone do tych produkowanych przez organizmy żywe. Ponadto samo życie zależy w znacznym stopniu' \
              ' od związków nieorganicznych. Bardzo wiele enzymów i innych białek takich jak hemoglobina wymaga do' \
              ' swojej aktywności obecności metali przejściowych.Obecnie nauką, która zajmuje się badaniem ' \
              'związków chemicznych występujących w żywych organizmach oraz ich przemianami jest biochemia, ' \
              'która jest powiązana zarówno z chemią organiczną jak i wieloma dyscyplinami biologii.Z drugiej ' \
              'strony okazało się, że wszystkie związki organiczne zawierają węgiel czterowartościowy (pomijając' \
              ' dwutlenek węgla i cyjanki, będące zw. nieorganicznymi), stąd obecnie definicja chemii organicznej ' \
              'to chemia wszystkich tych związków węgla, którymi nie zajmowała się wcześniej tradycyjna chemia' \
              ' nieorganiczna. Z powodu ogromnej liczby możliwych do otrzymania związków zawierających złożony ' \
              'szkielet węglowy mogą one posiadać bardzo różnorodne właściwości oraz zastosowania. Przykładowo' \
              ' praktycznie wszystkie stosowane obecnie barwniki, tworzywa sztuczne oraz leki to związki organiczne.'
    final = get_topics_doc(new_doc, "../data/", n_topics=3)
    print "Topic words"
    for idx, topic in enumerate(final[1]):
        print "{}: {}\n".format(idx, topic)
    print "Document keywords"
    for idx, topic in enumerate(final[0]):
        print "{}: {}\n".format(idx, topic)
