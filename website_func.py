from pathlib import Path
import shutil
from html.parser import HTMLParser
from bs4 import BeautifulSoup

lenFileName = len("000a3333ad24828769b6be5a5e1bdb4a.html")

#filename = "recipePages/000a3333ad24828769b6be5a5e1bdb4a.html"
def read_website(filename):
#     my_dir = "recipePages/"
#     my_file = my_dir + filename
    my_file = filename
# CTRL + /
#     f = open(my_file, "r")
#     first_line = f.readlines()[0]#.split("/")[1]
#     # retrieve the website in order to 
#     print(first_line.split("/")[2])
#     print(first_line)
#     f.close()

#### Not sure about the errors parameter :/
    website =""
    with open(my_file, "r") as f: # no close() needed
        soup = BeautifulSoup(f, "html.parser")
        first_line = soup.readlines()[0]#.split("/")[1]
        # remove www. as same website may have http://allrecipes and http://www.allrecipes
        website = str(first_line).split("/")[2].strip("www.")
        #print("website", website)
    return website
		
		
def retrieve_website_into_txt():
	# Create the folder of the sorted files by website
    p = Path("SortedFiles/")
    p.mkdir(parents=True, exist_ok=True)

	# Get all filenames (i.e. path) that are in recipePages folder with .html as extension
    pathlist = Path("recipePages/").glob('**/*.html')
    for path in pathlist:
         # because path is object not string
        path_in_str = str(path)
        website = read_website(path_in_str)
        # create the 
        destination = p / website 
        if not destination.exists():
            destination.mkdir(parents=True, exist_ok=True)
		######
		### SHOULD WE ADD THE FILE OR SIMPLY ADD THE NAME OF THE FILE IN A .TXT FILE ??? 
		
        destinationFile = destination / "file666.txt"
        with destinationFile.open("a") as fid:
			#print(path)
            fid.write(path_in_str + "\n")
            
def website_from_log(s):
    #s = BeautifulSoup(s)
    # remove www. as same website may have http://allrecipes and http://www.allrecipes
    website = str(s).split("/")[2].strip("www.")
    filename = str(s).split("http://")[0].rstrip() # to remove the tab
    # want to keep only the name as there may be other attributes 
    if len(filename) != lenFileName: # All file name have the same length
        filename =""
    #print(filename)
    return website, filename


# Sort the files according to their website and put their filenames altogether in a folder corresponding to a website domain
def sort_website_from_log(override=False):
    # Name of the folder containing the sorted website files
    p = Path("SortedFiles/")
    
    # If it already exists, we don't do anything. Except if override is true
    if not p.is_dir() or override:
        
        if override:
            shutil.rmtree(p) # Delete the folder and the files in it
            
        # Create the folder of the sorted files by website
        #p = Path("SortedFiles/")
        p.mkdir(parents=True, exist_ok=True)

        path_to_log = Path("recipePages/msg.log")

        with open(path_to_log, "r") as f:
            for line in f.readlines():
                web, file = website_from_log(line)
                if file == "": ## ignore this line
                    continue
                destination = p / web
                destination.mkdir(parents=True, exist_ok=True)
                destinationFile = destination / "filesName.txt"
                with destinationFile.open("a+") as fid:
                    fid.write(file + "\n")
    print("Finished sorting the files")
#     try:
#     loop.run_until_complete(bar())
# except KeyboardInterrupt:
#     print("It's ok")
# finally:
#     loop.stop()
#     loop.close()