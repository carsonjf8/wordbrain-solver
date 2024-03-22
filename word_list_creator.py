import pickle

def main() -> None:
    word_file_path = 'data/words_alpha.txt'

    word_len_dict = {}
    print('analyzing words')
    with open(word_file_path, 'r') as f:
        for word in f:
            word = word.strip()
            word_len = len(word)
            word_len_str = str(word_len)

            if word_len_str in word_len_dict:
                cur_list = word_len_dict[word_len_str]
                cur_list.append(word)
                word_len_dict[word_len_str] = cur_list
            else:
                word_len_dict[word_len_str] = [word]

    for key in word_len_dict.keys():
        with open(f'data/{key}.pickle', 'wb') as f:
            print(key, len(word_len_dict[key]))
            pickle.dump(word_len_dict[key], f)
    
    '''
    for key in word_len_dict.keys():
    with open(f'{key}.pickle', 'rb') as f:
        word_list = pickle.load(f)
        print(key, len(word_list))
    '''

if __name__ == '__main__':
    main()
