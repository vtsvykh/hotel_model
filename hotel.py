from datetime import datetime, timedelta
import ru_local


class Room:
    """
    Class of rooms.

    Args:
        number (str): number of room
        room_type (str): type of room
        capacity (str): capacity of room
        comfort_level (str): comfort level of room
        price_per_person (int): price per person
        current_guests (list): list of current quests
    """

    def __init__(self, number, room_type, capacity, comfort_level):
        self.number = number
        self.room_type = room_type
        self.capacity = capacity
        self.comfort_level = comfort_level
        self.price_per_person = self.calculate_price()
        self.current_guests = []

    def calculate_price(self):
        """
        Function of calculating price.
        :return: the final price
        """
        base_prices = {
            ru_local.ONE_PERSON: 2900.00,
            ru_local.TWO_PERSON: 2300.00,
            ru_local.JUNIOR_SUITE: 3200.00,
            ru_local.LUXURY: 4100.00
        }
        comfort_factors = {
            ru_local.STANDART: 1.0,
            ru_local.UP_STANDART: 1.2,
            ru_local.APARTMENT: 1.5
        }
        return base_prices[self.room_type] * comfort_factors[self.comfort_level]

    def is_available(self, date, days):
        """
        Function return room is available or not.
        :param date: check in date
        :param days: stay date
        :return: True or False
        """
        for guest_date, guest_days in self.current_guests:
            if (date <= guest_date + timedelta(days=guest_days) <= date + timedelta(days=days)) or \
                    (guest_date <= date <= guest_date + timedelta(days=guest_days)):
                return False
        return True

    def book(self, date, days, guests, meal):
        """
        Function of booking room.
        :param date: check in date
        :param days: stay date
        :param guests: number of guests
        :param meal: type of meal
        """
        self.current_guests.append((date, days))
        print(
            f'{ru_local.NUMBER} {self.number} {ru_local.SUCCESS_BOOK} {date.strftime("%d.%m.%Y")} {ru_local.ON} {days} {ru_local.DAY_FOR} {guests} {ru_local.GUESTS}.')


class BookingRequest:
    """
    Class of booking.

    Args:
        self.booking_date = booking_date
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.guests_count = guests_count
        self.check_in_date = check_in_date
        self.stay_days = stay_days
        self.budget = budget
    """

    def __init__(self, booking_date, last_name, first_name, middle_name, guests_count, check_in_date, stay_days,
                 budget):
        self.booking_date = booking_date
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.guests_count = guests_count
        self.check_in_date = check_in_date
        self.stay_days = stay_days
        self.budget = budget

    def __repr__(self):
        return f'{[self.booking_date, self.last_name, self.first_name, self.middle_name, self.guests_count, self.check_in_date, self.stay_days, self.max_price_per_person]}'


class AccommodationOption:
    def __init__(self, room, check_in_date, stay_days, guests_count, total_price, meal):
        self.room = room
        self.check_in_date = check_in_date
        self.stay_days = stay_days
        self.guests_count = guests_count
        self.total_price = total_price
        self.meal = meal
