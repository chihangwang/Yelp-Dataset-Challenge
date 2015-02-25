combined_file = open('combine', 'r')

benchmark_mark = 200

for line in combined_file:
    try:

        line = line.strip()
        review_cnt = int(line.split(' ')[1])

        if review_cnt >= benchmark_mark:
            print line

    except ValueError as e:
        print e

combined_file.close()
