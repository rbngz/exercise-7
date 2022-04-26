import imageio
import glob


# Utitlity to create a GIF from the graph images

images = []

filenames = glob.glob("/Users/rubengonzalez/Coding/exercise-7/graphs/*.png")
filenames.reverse()
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave("movie3.gif", images)
