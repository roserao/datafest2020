import pandas as pd
import os
import glob

if __name__ == "__main__":
    # hashtag list of interest
    list = 'hashtag_list.txt'
    f = open(list, "r")
    list_of_interest = f.readlines()
    for i in range(len(list_of_interest)):
        list_of_interest[i] = list_of_interest[i].replace("\n", "")

    # output csv
    output = "daily_hashtag_count.csv"
    o = open(output, "w")

    # input the data
    path = '/Users/rossierao/Desktop/Datafest/SampleTest/data/'
    csv_dir = path + '*.CSV'
    inputs = glob.glob(csv_dir)
    for input in inputs:
        date_loc = input.find("2020-")
        date = input[date_loc:date_loc + 10]
        data = pd.read_csv(input)
        # select only the English version
        data = data.query("lang == 'en'")

        # sample size
        #sample_data = data.sample(frac=0.01, replace=False, random_state = 706)
        #o.write("data size: " + str(data.shape[0]) + "\n")
        #o.write("sample size: " + str(sample_data.shape[0]) + "\n")
        #o.write("\n")

        num_tweets = data.shape[0]
        hashtag = data.text.str.findall(r'#.*?(?=\s|$)').explode().str.lower().str.replace('[^a-z0-9#]', '')
        counts = hashtag.value_counts()
        count_of_interest = []
        for x in list_of_interest:
            try:
                count_of_interest.append(int(counts.loc[x]/num_tweets*1000000))
            except:
                print("No hashtag today: " + x + " " + input, end = "\n")
                count_of_interest.append(0)

        # write to csv
        for i in range(len(list_of_interest)):
            o.write(list_of_interest[i] + "," + str(count_of_interest[i]) + "," + date + "\n")

        print("Successful! " + input, end = "\n")

    o.close()




