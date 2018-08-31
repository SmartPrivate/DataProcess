import logging
import DataModel
import DBConnector
import pandas
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as pyplot
import time
import xlwt

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


def write_test_model_to_file(filename, data_model):
    models = DBConnector.query_all(data_model)
    writer = open('K_means_result/word_cut_file/{0}.csv'.format(filename), 'a')
    for model in models:
        if not model.words_vector:
            continue
        line_list = []
        vectors = model.words_vector.split(',')
        if filename == 'zhihu':
            line_list.append(str(model.sid))
        else:
            line_list.append(str(model.weibo_sid))
        for vector in vectors:
            line_list.append(vector)
        line = ','.join(line_list)
        line = line + '\n'
        writer.write(line)
    writer.close()


def calculate_sse(filename, start, stop, step):
    test_data_frame = pandas.read_csv('K_means_result/word_cut_file/{0}.csv'.format(filename), header=None)
    result_writer = open(
        'K_means_result/{0}_sse_{1}.txt'.format(filename, time.strftime("%Y%m%d_%H%M%S", time.localtime())), 'a')
    print(test_data_frame)
    sse = []
    for i in range(start, stop, step):
        estimator = KMeans(n_clusters=i)
        estimator.fit(test_data_frame)
        sse.append(estimator.inertia_)
        print('完成{0}'.format(str(i)))
        result_writer.write(str(i) + ',' + str(estimator.inertia_) + '\n')
    result_writer.close()
    x = range(start, stop, step)
    pyplot.xlabel('K value')
    pyplot.ylabel('SSE')
    pyplot.plot(x, sse, 'o-')
    pyplot.show()


def calculate_silhouette_coefficient(filename, start, stop, step):
    scores = []
    result_writer = open(
        'K_means_result/{0}_sc_{1}.txt'.format(filename, time.strftime("%Y%m%d_%H%M%S", time.localtime())), 'a')
    for i in range(start, stop, step):
        test_data_frame = pandas.read_csv('K_means_result/word_cut_file/{0}.csv'.format(filename), header=None)
        estimator = KMeans(n_clusters=i)
        estimator.fit(test_data_frame)
        sc = silhouette_score(test_data_frame, estimator.labels_)
        scores.append(sc)
        print('完成{0}'.format(str(i)))
        result_writer.write(str(i) + ',' + str(sc) + '\n')
    result_writer.close()
    x = range(start, stop, step)
    pyplot.xlabel('K value')
    pyplot.ylabel('Silhouette Coefficient')
    pyplot.plot(x, scores, 'o-')
    pyplot.show()


def calculate_sse_and_silhouette_coefficient(filename, start, stop, step):
    calculate_sse(filename, start, stop, step)
    calculate_silhouette_coefficient(filename, start, stop, step)


def calculate_kmeans(filename, k):
    test_data_frame = pandas.read_csv('K_means_result/word_cut_file/{0}.csv'.format(filename), header=None, index_col=0)
    zhihu_sid_list = []
    lines = open('K_means_result/word_cut_file/{0}.csv'.format(filename), 'r').readlines()
    for line in lines:
        zhihu_sid_list.append(line.split(',')[0])
    estimator = KMeans(n_clusters=k)
    result = estimator.fit_predict(test_data_frame)
    result_cluster: list[list[str]] = []
    for cluster_count in range(k):
        result_cluster.append([])
    for i in range(len(zhihu_sid_list)):
        result_cluster[result[i]].append(zhihu_sid_list[i])
    return result_cluster


def kmeans_result_save(filename, k):
    results = calculate_kmeans(filename=filename, k=k)
    workbook = xlwt.Workbook(encoding='gbk')
    time_str = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    k_count = 0
    for result in results:
        models = DBConnector.get_sid_in(result, filename)
        worksheet = workbook.add_sheet('cluster_{0}'.format(str(k_count + 1)))
        model_count = 0
        for model in models:
            if filename == 'zhihu':
                worksheet.write(model_count, 0, model.sid)
                worksheet.write(model_count, 1, model.zhihu_answer)
            else:
                worksheet.write(model_count, 0, model.weibo_sid)
                worksheet.write(model_count, 1, model.weibo_content)
            model_count = model_count + 1
        k_count = k_count + 1
    workbook.save('K_means_result/{2}_kmeans/{2}_k{0}_{1}.xls'.format(str(k), time_str, filename))


# calculate_sse('weibo', start=10, stop=210, step=10)

result_sid_list = calculate_kmeans('weibo', k=70)
writer = open('weibo_sid.txt', 'a')
for sid in result_sid_list:
    line = ','.join(sid) + '\n'
    writer.write(line)
writer.close()
