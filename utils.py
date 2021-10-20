import pandas as pd
import re
from os.path import exists


def feature_to_binary(feature, data_set):
    features = []
    for each_row in data_set[feature]:
        if pd.notna(each_row):
            each_feature = re.split(r', \s*', each_row)
            features.extend(each_feature)
    
    feature_list = sorted(set(features))
    feature_in_binary = [[0] * 0 for i in range(len(set(features)))]
    for each_row in data_set[feature]:
        count  = 0
        for a_feature in feature_list:
            if pd.isna(each_row):
                feature_in_binary[count].append(0.0)
            elif a_feature in each_row:
                feature_in_binary[count].append(1.0)
            else:
                feature_in_binary[count].append(0.0)
            count += 1
    feature_in_binary = pd.DataFrame(feature_in_binary).transpose()
    return feature_in_binary

def get_feature_binary(feature, data_set, data_set_name):
    file_path = f"binary_{feature}_{data_set_name}.csv"
    if exists(file_path):
        binary_feature = pd.read_csv(file_path)
    else:
        binary_feature = feature_to_binary(feature, data_set)
        binary_feature.to_csv(path_or_buf=file_path, index=False)
    return binary_feature

    # try:
    #     ## file does not exist
    #     file = open(file_path, "x")
    #     binary_feature = feature_to_binary(feature, data_set)
    #     binary_feature.to_csv(path_or_buf=file_path, index=False)
    #     #file.write(binary_feature)
    #     file.close()
    # except Exception as e:
    #     ## file exist
    #     # file = open(file_path, "r")
    #     binary_feature = pd.read_csv(file_path)
    #     # binary_feature = file.read()
    #     # file.close()


def combine_data_binaries(binary_features, data_set):
    file_path = f"binary_{data_set}.csv"
    if exists(file_path):
        combined_binaries = pd.read_csv(file_path)
    else:
        combined_binaries = pd.concat(binary_features, axis = 1, ignore_index = True)
        combined_binaries.to_csv(path_or_buf=file_path, index=False)
    return combined_binaries
    # try:
    #     file = open(file_path, "x")
    #     combined_binaries = pd.concat(binary_features, axis =1, ignore_index = True)
    #     file.write(combined_binaries)
    # except Exception as e:
    #     file = open(file_path, "r")
    #     combined_binaries = file.read()
    #     file.close()



# def recommender(search):
#     cs_list = []
#     binary_list = []
#     if search in movies['title'].values:
#         idx = movies[movies['title'] == search].index.item()
#         for i in binary_movies.iloc[idx]:
#             binary_list.append(i)
#         point1 = np.array(binary_list).reshape(1, -1)
#         point1 = [val for sublist in point1 for val in sublist]    
#         for j in range(len(movies)):
#             binary_list2 = []
#             for k in binary_movies.iloc[j]:
#                 binary_list2.append(k)
#             point2 = np.array(binary_list2).reshape(1, -1)
#             point2 = [val for sublist in point2 for val in sublist]
#             dot_product = np.dot(point1, point2)
#             norm_1 = np.linalg.norm(point1)
#             norm_2 = np.linalg.norm(point2)
#             cos_sim = dot_product / (norm_1 * norm_2)
#             cs_list.append(cos_sim)
#         movies_copy = movies.copy()
#         movies_copy['cos_sim'] = cs_list
#         results = movies_copy.sort_values('cos_sim', ascending=False)
#         results = results[results['title'] != search]    
#         top_results = results.head(5)
#         return(top_results)
#     elif search in tv['title'].values:
#         idx = tv[tv['title'] == search].index.item()
#         for i in binary_tv.iloc[idx]:
#             binary_list.append(i)
#         point1 = np.array(binary_list).reshape(1, -1)
#         point1 = [val for sublist in point1 for val in sublist]
#         for j in range(len(tv)):
#             binary_list2 = []
#             for k in binary_tv.iloc[j]:
#                 binary_list2.append(k)
#             point2 = np.array(binary_list2).reshape(1, -1)
#             point2 = [val for sublist in point2 for val in sublist]
#             dot_product = np.dot(point1, point2)
#             norm_1 = np.linalg.norm(point1)
#             norm_2 = np.linalg.norm(point2)
#             cos_sim = dot_product / (norm_1 * norm_2)
#             cs_list.append(cos_sim)
#         tv_copy = tv.copy()
#         tv_copy['cos_sim'] = cs_list
#         results = tv_copy.sort_values('cos_sim', ascending=False)
#         results = results[results['title'] != search]    
#         top_results = results.head(5)
#         return(top_results)
#     else:
#         return("Title not in dataset. Please check spelling.")







# ### convert the movie features to a binary format
# binary_actors = get_feature_binary("cast", movies)
# binary_directors = get_feature_binary("director", movies)
# binary_countries = get_feature_binary("country", movies)
# binary_genres = get_feature_binary("listed_in", movies)
# binary_ratings = get_feature_binary("rating", movies)


# ## concatenate these binaries
# binary_movies = combine_data_binaries([binary_actors, binary_directors, binary_countries, binary_genres], "movies")


# ### convert the tv features to a binary format
# binary_actors_tv = get_feature_binary("cast", tv)
# binary_countries_tv = get_feature_binary("country", tv)
# binary_genres_tv = get_feature_binary("listed_in", tv)
# binary_ratings_tv = get_feature_binary("rating", tv)

# #concatenate these binaries...
# binary_tv = combine_data_binaries([binary_actors_tv, binary_countries_tv, binary_genres_tv], "tv")
