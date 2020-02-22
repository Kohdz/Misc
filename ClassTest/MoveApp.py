import movieModel

toy_story = movieModel.Movie(
    "ToyStory", "A Story Of Toys", "toy.jpg", "youtube.com")

print(toy_story.storyline)

# toy_story.show_trailer()

print(movieModel.Movie.VALID_RATINGS)
print(movieModel.Movie.__dict__)
