from datetime import timedelta
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
        condition (bool): True or False

    """

    def __init__(self, number, room_type, capacity, comfort_level):
        """
        The function sets attributes for an instance of a class.
        :param number (str): number of room
        :param room_type (str): type of room
        :param capacity (str): capacity of room
        :param comfort_level (str): comfort level of room
        """
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
        :param date (str): check in date
        :param days (str): stay date
        :return: True or False
        """
        for guest_date, guest_days in self.current_guests:
            if (date <= guest_date + timedelta(days=guest_days) <= date + timedelta(days=days)) or \
                    (guest_date <= date <= guest_date + timedelta(days=guest_days)):
                return False
        return True

    def book(self, date, days, guests):
        """
        Function of booking room.
        :param date (str): check in date
        :param days (str): stay date
        :param guests (str): number of guests
        """
        self.current_guests.append((date, days))
        print(
            f'{ru_local.NUMBER} {self.number} {ru_local.SUCCESS_BOOK} {date.strftime("%d.%m.%Y")} {ru_local.ON} {days} {ru_local.DAY_FOR} {guests} {ru_local.GUESTS}.')

    def __str__(self):
        """
        Outputs a string in a readable format.
        """
        return f'{self.number} {self.room_type} {self.capacity} {self.comfort_level} {self.price_per_person} {self.current_guests}'

    def __repr__(self):
        return self.__str__()


class BookingRequest:
    """
    Class of booking.

    Args:
        booking_date (str): date of booking
        last_name (str): surname client
        first_name (str): name client
        middle_name (str): patronomic client
        guests_count (str): number of guests
        check_in_date (str): date of entry
        stay_days (str):  number day on hotel
        budget (str): client's budget
    """

    def __init__(self, booking_date, last_name, first_name, middle_name, guests_count, check_in_date, stay_days,
                 budget):
        """
        The function sets attributes for an instance of a class.
        :param booking_date (str): date of booking
        :param last_name (str): surname client
        :param first_name (str): name client
        :param middle_name (str): patronomic client
        :param guests_count (str): number of guests
        :param check_in_date (str): date of entry
        :param stay_days (str): number day on hotel
        :param budget (str): client's budget
        """
        self.booking_date = booking_date
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.guests_count = guests_count
        self.check_in_date = check_in_date
        self.stay_days = stay_days
        self.budget = budget

    def __str__(self):
        """
        Outputs a string in a readable format.
        """
        return f'{[self.booking_date, self.last_name, self.first_name, self.middle_name, self.guests_count, self.check_in_date, self.stay_days, self.budget]}'

    def __repr__(self):
        """
        Creates a string representation of an object.
        """
        return self.__str__()


class AccommodationOption:
    """
    Class of possible placement options.

    Args:
        room (str): number of room
        check_in_date (str): date of entry
        stay_days (str): number day on hotel
        guests_count (str): number of guests
        total_price (str): total price
        meal (str): type of meal
    """

    def __init__(self, room, check_in_date, stay_days, guests_count, total_price, meal):
        """
        The function sets attributes for an instance of a class.
        :param room (str): number of room
        :param check_in_date (str): date of entry
        :param stay_days (str): number day on hotel
        :param guests_count (str): number of guests
        :param total_price (str): total price
        :param meal (str): type of meal
        """
        self.room = room
        self.check_in_date = check_in_date
        self.stay_days = stay_days
        self.guests_count = guests_count
        self.total_price = total_price
        self.meal = meal

    def __str__(self):
        """
        Outputs a string in a readable format.
        """
        return f'{self.room} {self.check_in_date} {self.stay_days} {self.guests_count} {self.total_price} {self.meal}'

    def __repr__(self):
        """
        Creates a string representation of an object.
        """
        return self.__str__()
