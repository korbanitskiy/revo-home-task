import pytest
from nester.nest import groupify_arr, create_group


@pytest.fixture()
def input_data():
    return [
        {"country": "US", "city": "Boston", "currency": "USD", "amount": 100},
        {"country": "FR", "city": "Paris",  "currency": "EUR", "amount": 20},
        {"country": "FR", "city": "Lyon",   "currency": "EUR", "amount": 11.4},
        {"country": "ES", "city": "Madrid", "currency": "EUR", "amount": 8.9},
        {"country": "UK", "city": "London", "currency": "GBP", "amount": 12.2},
        {"country": "UK", "city": "London", "currency": "FBP", "amount": 10.9}
    ]


def test_gropify_empty_array():
    assert groupify_arr([], 'test') == {}


def test_gropify_by_country(input_data):
    assert groupify_arr(input_data, 'country') == {
        'ES': [{'amount': 8.9, 'city': 'Madrid', 'currency': 'EUR'}],
        'FR': [{'amount': 20, 'city': 'Paris', 'currency': 'EUR'},
               {'amount': 11.4, 'city': 'Lyon', 'currency': 'EUR'}],
        'UK': [{'amount': 12.2, 'city': 'London', 'currency': 'GBP'},
               {'amount': 10.9, 'city': 'London', 'currency': 'FBP'}],
        'US': [{'amount': 100, 'city': 'Boston', 'currency': 'USD'}]
    }


def test_groupify_by_city(input_data):
    assert groupify_arr(input_data, 'city') == {
        'Boston': [{'amount': 100, 'country': 'US', 'currency': 'USD'}],
        'London': [{'amount': 12.2, 'country': 'UK', 'currency': 'GBP'},
                   {'amount': 10.9, 'country': 'UK', 'currency': 'FBP'}],
        'Lyon': [{'amount': 11.4, 'country': 'FR', 'currency': 'EUR'}],
        'Madrid': [{'amount': 8.9, 'country': 'ES', 'currency': 'EUR'}],
        'Paris': [{'amount': 20, 'country': 'FR', 'currency': 'EUR'}]
    }


def test_groupify_by_currency(input_data):
    assert groupify_arr(input_data, 'currency') == {
        'EUR': [{'amount': 20, 'city': 'Paris', 'country': 'FR'},
                {'amount': 11.4, 'city': 'Lyon', 'country': 'FR'},
                {'amount': 8.9, 'city': 'Madrid', 'country': 'ES'}],
        'FBP': [{'amount': 10.9, 'city': 'London', 'country': 'UK'}],
        'GBP': [{'amount': 12.2, 'city': 'London', 'country': 'UK'}],
        'USD': [{'amount': 100, 'city': 'Boston', 'country': 'US'}]
    }


def test_create_group_by_country_city_currency(input_data):
    assert create_group(input_data, ['country', 'city', 'currency']) == {
        'ES': {'Madrid': {'EUR': [{'amount': 8.9}]}},
        'FR': {'Lyon': {'EUR': [{'amount': 11.4}]},
               'Paris': {'EUR': [{'amount': 20}]}},
        'UK': {'London': {'FBP': [{'amount': 10.9}], 'GBP': [{'amount': 12.2}]}},
        'US': {'Boston': {'USD': [{'amount': 100}]}}
    }
