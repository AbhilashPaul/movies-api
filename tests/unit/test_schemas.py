from datetime import date

import pytest
from marshmallow import ValidationError

from api.constants import CHARACTER_LIMIT_TITLE, CHARACTER_LIMIT_DESCRIPTION
from api.schemas import validate_character_count, validate_title, validate_description, validate_release_year


def test_validate_character_count():
    validate_character_count('abcd', 5)


def test_validate_character_count_raises_exception_when_validation_fails():
    with pytest.raises(ValidationError) as e:
        validate_character_count('abcdef', 5)
        assert str(e) == "Text input must be less than 5 characters."


def test_validate_title():
    validate_title('fake title')


def test_validate_title_raises_exception_when_validation_fails():
    with pytest.raises(ValidationError) as e:
        validate_title('''fake long title: Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
        sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.''')
        assert str(e) == f"Text input must be less than {CHARACTER_LIMIT_TITLE} characters."


def test_validate_description():
    validate_description('fake description')


def test_validate_description_raises_exception_when_validation_fails():
    with pytest.raises(ValidationError) as e:
        validate_description(
            '''fake long description: Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Tristique risus 
            nec feugiat in fermentum posuere urna nec tincidunt. Odio morbi quis commodo odio 
            aenean sed adipiscing diam. Rhoncus dolor purus non enim praesent elementum facilisis 
            leo vel. Habitant morbi tristique senectus et netus et malesuada. Quisque id diam vel 
            quam. Non curabitur gravida arcu ac. Ultricies mi quis hendrerit dolor.''')
        assert str(e) == f"Text input must be less than {CHARACTER_LIMIT_DESCRIPTION} characters."


def test_validate_release_year():
    validate_release_year(date.today().year-1)


def test_validate_release_year_raises_exception_when_validation_fails():
    with pytest.raises(ValidationError) as e:
        validate_release_year(date.today().year+1)
        assert str(e) == "Year of release must be less than or equal to current year."
