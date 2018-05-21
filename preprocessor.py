# preprocessor.py

import argparse
import sys

def preprocess(in_filename, stop_filename, out_filename=None):

    stopword_counter = 0
    shortword_counter = 0

    if out_filename is None:
        out_filename = 'preprocessed_'+in_filename

    junk_charset = ''.join( chr(i) for i in range(33, 127)
                            if not chr(i).isalpha() )  # 39 is '
    transit_map = str.maketrans(junk_charset, ' ' * len(junk_charset))

    stopword_file = open(stop_filename, 'r')
    stopwords_set = set()
    for line in stopword_file:
        stopwords_set.add(line.strip())
    stopword_file.close()

    output_file = open(out_filename,'w')
    with open(in_filename, 'r') as raw_file:
        for line in raw_file:

            draft1 = ''
            draft2 = ''
            output = ''

            line = line.lower()
            for word in line.split():
                if word in stopwords_set:
                    draft1 += ' '
                    stopword_counter += 1
                elif len(word) < 3:
                    draft1 += ''
                    shortword_counter += 1
                else:
                    draft1 += word + ' '

            draft2 = draft1.translate(transit_map)

            for word in draft2.split():
                if word in stopwords_set:
                    output += ' '*len(word)
                    stopword_counter += 1
                elif len(word) < 3 or word.startswith('\'') or\
                        word.startswith('\"'):
                    output += ''
                    shortword_counter += 1
                else:
                    output += word + ' '

            output = ' '.join(output.split())
            output_file.write(output+'\n')

    raw_file.close()
    output_file.close()

    print("Preprocessing stats for the input file: " + str(in_filename))
    print("Stopwords removed: " + str(stopword_counter))
    print("Short words removed: " + str(shortword_counter))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='prepossesses a text file for'
                                                 ' further indexing purposes.')

    parser.add_argument('input', help='input text file address/name')
    parser.add_argument('stopwords', help='stopword text file address/name')
    parser.add_argument('--output', dest='output', help='output processed'
                                                        ' file name')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    if not args.input:
        raise ImportError

    if args.output:
        preprocess(args.input,args.stopwords,args.output)
    else:
        preprocess(args.input,args.stopwords)




