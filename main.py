import argparse
from Scripts import gettingTut
from Scripts import gettingSub
from Scripts import thirdAlgo
from Scripts import topicSim
from Scripts import docSimilarity
from Scripts import clean



if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-t", "--tlink", type=str, help="base link of tutorialpoints tutorial like : \
                            https://www.tutorialspoint.com/html/html_overview.htm ")

    parser.add_argument("-y", "--ytlink", type=str, help="keywords combination for your youtube search like : \
                            HTML TUTORIALS corrosponding to your tutorialspoint base case")

    parser.add_argument("-c", "--clear", type=int, choices=[0,1], default=0, help="You want to delete all of the \
                            temporary files which was generated during the process, 0 for yes, 1 for no")

    args = parser.parse_args()

    #To download the subtitle from tutorials 
    obj = gettingTut.gettingTut(args.tlink)
    obj.saveData()

    # To download subtitle from youtube as playlist for first two algorithms
    obj = gettingSub.gettingSub(args.ytlink)
    obj.Get_subtitle()

    #Running different algoruthms to find out relevent results
    docSimilarity.docSimilarity()
    topicSim.topicSim()    
    thirdAlgo.thirdAlgo()    
    
    # to clean the directory
    if args.clear == 1:
        clean.clearAll()
