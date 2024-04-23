import hotel
import random
from datetime import datetime, timedelta
import ru_local


def load_rooms(filename):
    """
    Function of loading information about room data.
    :param filename: name of file
    :return: list of rooms
    """
    rooms = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            room_info = line.strip().split()
            room = hotel.Room(int(room_info[0]), room_info[1], int(room_info[2]), room_info[3])
            rooms.append(room)
    return rooms


def load_booking_requests(filename):
    """
    Function of loading information about booking data.
    :param filename: name of file
    :return: list of booking
    """
    booking_requests = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            booking_info = line.strip().split()
            booking_date = datetime.strptime(booking_info[0], '%d.%m.%Y')
            check_in_date = datetime.strptime(booking_info[5], '%d.%m.%Y')
            request = hotel.BookingRequest(booking_date, booking_info[1], booking_info[2], booking_info[3],
                                           int(booking_info[4]), check_in_date, int(booking_info[6]),
                                           float(booking_info[7]))
            booking_requests.append(request)

    return booking_requests


def process_booking_requests(rooms, booking_requests, current_date):
    """
    Function generate process of booking.
    :param rooms (list): list of rooms
    :param booking_requests (list): list of booking
    :param current_date (datetime): current date
    :return: dictionary with booking on date
    """
    booked_rooms_by_date = {}
    for request in booking_requests:
        accommodation_options = []

        for room in rooms:
            if room.is_available(request.check_in_date, request.stay_days) and \
                    room.capacity >= request.guests_count:
                total_price = hotel.Room.calculate_price(room)
                meal_prices = {
                    ru_local.WITHOUT_MEALS: 0.00,
                    ru_local.BREAKFAST: 280.00,
                    ru_local.HALF_BOARD: 1000.00
                }
                if request.budget - total_price >= meal_prices[ru_local.BREAKFAST]:
                    if request.budget - total_price >= meal_prices[ru_local.HALF_BOARD]:
                        accommodation_options.append(
                            hotel.AccommodationOption(room, request.check_in_date, request.stay_days,
                                                      request.guests_count,
                                                      total_price + meal_prices[ru_local.HALF_BOARD],
                                                      ru_local.HALF_BOARD))
                    else:
                        accommodation_options.append(
                            hotel.AccommodationOption(room, request.check_in_date, request.stay_days,
                                                      request.guests_count,
                                                      total_price + meal_prices[ru_local.BREAKFAST],
                                                      ru_local.BREAKFAST))
                else:
                    accommodation_options.append(
                        hotel.AccommodationOption(room, request.check_in_date, request.stay_days,
                                                  request.guests_count,
                                                  total_price + meal_prices[ru_local.WITHOUT_MEALS],
                                                  ru_local.WITHOUT_MEALS))

        if accommodation_options:
            accommodation_options.sort(key=lambda x: x.total_price)
            best_option = accommodation_options[0]

            if random.random() > 0.25:
                best_option.room.book(best_option.check_in_date, best_option.stay_days, best_option.guests_count)
                for i in range(best_option.stay_days):
                    date = best_option.check_in_date + timedelta(days=i)
                    if date in booked_rooms_by_date:
                        booked_rooms_by_date[date].append(best_option.room.number)
                    else:
                        booked_rooms_by_date[date] = [best_option.room.number]
            else:
                print(f'{ru_local.CLIENT} {request.last_name} {request.first_name} {ru_local.FAIL}.')
        else:
            print(
                f'{ru_local.REQUEST} {request.last_name} {request.first_name} {ru_local.ON} {request.guests_count}'
                f'{ru_local.PPL_DATE} {request.check_in_date.strftime("%d.%m.%Y")} {ru_local.NO_AVBL_ROOM}')

    return booked_rooms_by_date


def calculate_revenue(booked_rooms_by_date, rooms):
    """
    Function calculate revenue.
    :param booked_rooms_by_date (dict): dictionary with booking on date
    :param rooms (list): list of rooms
    :return: total revenue, missed revenue, available rooms
    """
    total_revenue = 0
    missed_revenue = 0
    total_rooms = len(rooms)
    occupied_rooms = set()

    for date, room_numbers in booked_rooms_by_date.items():
        total_revenue += sum([room.price_per_person for room in rooms if room.number in room_numbers])
        occupied_rooms.update(room_numbers)

    missed_revenue = sum([room.price_per_person for room in rooms if room.number not in occupied_rooms])

    return total_revenue, missed_revenue, total_rooms - len(occupied_rooms)


def print_report(booked_rooms_by_date, rooms, current_date):
    """
    Function print report.
    :param booked_rooms_by_date (dict): dictionary with booking on date
    :param rooms (list): list of rooms
    :param current_date (datetime): current date
    """
    total_revenue, missed_revenue, empty_rooms = calculate_revenue(booked_rooms_by_date, rooms)
    total_rooms = len(rooms)
    print('\n')
    print(f'{ru_local.REPORT} {current_date.strftime("%d.%m.%Y")}:')
    print(f'{ru_local.OCCPD_ROOM}: {total_rooms - empty_rooms}')
    print(f'{ru_local.AVBL_ROOM}: {empty_rooms}')
    print(f'{ru_local.WORKLOAD_ROOM}')

    for room_type in set([room.room_type for room in rooms]):
        if current_date in booked_rooms_by_date.keys():
            occupied_rooms = sum([1 for room in rooms if
                                  room.room_type == room_type and room.number in booked_rooms_by_date[current_date]])
        else:
            occupied_rooms = 0
        total_rooms_type = sum([1 for room in rooms if room.room_type == room_type])

        print(f'{room_type}: {round(occupied_rooms / total_rooms_type * 100, 2)}%')
    print(f'{ru_local.WORKLOAD_HOTEL} {round((total_rooms - empty_rooms) / total_rooms * 100, 2)}%')
    print(f'{ru_local.INCOME_DAY}: {total_revenue} {ru_local.CURRENCY}.')
    print(f'{ru_local.MISS_INCOME}: {missed_revenue} {ru_local.CURRENCY}.')
    print('\n')


"""
            occupied_rooms = sum([1 for room in rooms if
                                  room.room_type == room_type and room.number in booked_rooms_by_date[current_date]])
            r = sum([1 for room in rooms if room.current_guests != []])
            itog = occupied_rooms + r
            print(itog)"""

def main():
    """
    Function of main process.
    """
    rooms = load_rooms("fund.txt")
    booking_requests = load_booking_requests("booking.txt")
    start_date = datetime(2020, 3, 1)
    end_date = start_date + timedelta(days=1)
    current_date = start_date
    for day in range(1, 31):
        order = []
        for i in booking_requests:
            if day == i.booking_date.day:
                order.append(i)
        print_report(process_booking_requests(rooms, order, datetime(2020, 3, day)), rooms, current_date)
        current_date += timedelta(days=1)


if __name__ == "__main__":
    main()
