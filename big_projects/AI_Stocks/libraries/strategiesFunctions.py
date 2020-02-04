import progressbar

# Analitics functions for calculating effectivness of every strategy
class strategiesFunctions():
    # 3 Trends based strategy Buy, Sell, Stall
    def trendStrategy(data, calculate_interval, not_stall_procentage):
        # Variables
        data_div = 1000
        effectivness = 0
        stall_counter = 0
        bar = progressbar.ProgressBar(maxval=int(len(data)/data_div)).start()
        
        print(" - Calculating Trends Strategy - : ")
        for main_iterator in range(calculate_interval + 2, len(data)-2):
            # Variables
            determinator_up = 0
            determinator_down = 0
            stall = True

            for past_data_iterator in range(1, calculate_interval + 1):
                if data[main_iterator - past_data_iterator] <= data[main_iterator - past_data_iterator - 1]:
                    determinator_down += 1
                else:
                    determinator_up += 1
            if determinator_up/(determinator_down + determinator_up) >= not_stall_procentage or determinator_down/(determinator_down + determinator_up) >= not_stall_procentage:
                stall = False

            #print(" - " + str(data[main_iterator]) + " : " + str(data[main_iterator-1]))

            if not stall and determinator_up > determinator_down:
                if data[main_iterator] >= data[main_iterator - 1] or data[main_iterator + 1] >= data[main_iterator - 1] or data[main_iterator + 2] >= data[main_iterator - 1]:

                        effectivness += 1
            elif not stall and determinator_down > determinator_up:
                if data[main_iterator] <= data[main_iterator - 1] or data[main_iterator + 1] <= data[main_iterator - 1] or data[main_iterator + 2] <= data[main_iterator - 1]:
                        effectivness += 1

            if stall:
                stall_counter += 1

            if main_iterator%data_div == 0:
                bar.update(main_iterator/data_div)
        
        bar.finish()
        return effectivness/(len(data) - calculate_interval - stall_counter)