from api.models import Movie


class TestMovie:
    def test_movie_constructor(self):
        fake_title = "fake_title"
        fake_description = "fake_description"
        movie = Movie(fake_title, fake_description, 1989, 95, 6.5)
        assert movie.title == fake_title
        assert movie.description == fake_description
        assert movie.release_year == 1989
        assert movie.duration_minutes == 95
        assert movie.rating == 6.5
        assert movie.likes == 0
        assert movie.dislikes == 0

