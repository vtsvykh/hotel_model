import random
from datetime import datetime, timedelta

class Room:
    def __init__(self, number, room_type, capacity, comfort_level):
        self.number = number
        self.room_type = room_type
        self.capacity = capacity
        self.comfort_level = comfort_level
        self.price_per_person = self.calculate_price()
        self.current_guests = []

    def calculate_price(self):
        base_prices = {
            "одноместный": 2900.00,
            "двухместный": 2300.00,
            "полулюкс": 3200.00,
            "люкс": 4100.00
        }
        comfort_factors = {
            "стандарт": 1.0,
            "стандарт_улучшенный": 1.2,
            "апартамент": 1.5
        }
        return base_prices[self.room_type] * comfort_factors[self.comfort_level]

    def is_available(self, date, days):
        for guest_date, guest_days in self.current_guests:
            if (date <= guest_date + timedelta(days=guest_days) <= date + timedelta(days=days)) or \
                    (guest_date <= date <= guest_date + timedelta(days=guest_days)):
                return False
        return True

    def book(self, date, days, guests, meal):
        self.current_guests.append((date, days))
        print(f"Номер {self.number} успешно забронирован с {date.strftime('%d.%m.%Y')} на {days} дней для {guests} гостей. "
              f"Тип питания: {meal}")

class BookingRequest:
    def __init__(self, booking_date, last_name, first_name, middle_name, guests_count, check_in_date, stay_days, max_price_per_person):
        self.booking_date = booking_date
        self.last_name = last_name
        self.first_name = first_name
        self.middle_name = middle_name
        self.guests_count = guests_count
        self.check_in_date = check_in_date
        self.stay_days = stay_days
        self.max_price_per_person = max_price_per_person

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

def load_rooms(filename):
    rooms = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            room_info = line.strip().split()
            room = Room(int(room_info[0]), room_info[1], int(room_info[2]), room_info[3])
            rooms.append(room)
    return rooms

def load_booking_requests(filename):
    booking_requests = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            booking_info = line.strip().split()
            booking_date = datetime.strptime(booking_info[0], '%d.%m.%Y')
            check_in_date = datetime.strptime(booking_info[5], '%d.%m.%Y')
            request = BookingRequest(booking_date, booking_info[1], booking_info[2], booking_info[3],
                                      int(booking_info[4]), check_in_date, int(booking_info[6]),
                                      float(booking_info[7]))
            booking_requests.append(request)

    return booking_requests

def process_booking_requests(rooms, booking_requests, current_date):
    booked_rooms_by_date = {}
    for request in booking_requests:
        if request.check_in_date <= current_date:
            accommodation_options = []

            for room in rooms:
                if room.is_available(request.check_in_date, request.stay_days) and \
                        room.capacity >= request.guests_count and \
                        Room.calculate_price(room) <= request.max_price_per_person:
                    total_price = Room.calculate_price(room)
                    meal_prices = {
                        "Без питания": 0.00,
                        "Завтрак": 280.00,
                        "Полупансион": 1000.00
                    }
                    for meal, price in meal_prices.items():
                        if price <= request.max_price_per_person:
                            accommodation_options.append(AccommodationOption(room, request.check_in_date, request.stay_days,
                                                                              request.guests_count, total_price, meal))

            if accommodation_options:
                accommodation_options.sort(key=lambda x: x.total_price)
                best_option = accommodation_options[0]

                if random.random() > 0.25:
                    best_option.room.book(best_option.check_in_date, best_option.stay_days, best_option.guests_count, best_option.meal)
                    for i in range(best_option.stay_days):
                        date = best_option.check_in_date + timedelta(days=i)
                        if date in booked_rooms_by_date:
                            booked_rooms_by_date[date].append(best_option.room.number)
                        else:
                            print('ghbdtn')
                            booked_rooms_by_date[date] = [best_option.room.number]
                else:
                    print(f"Клиент {request.last_name} {request.first_name} отказался от бронирования.")
            else:
                print(f"Для заявки {request.last_name} {request.first_name} на {request.guests_count} "
                      f"человек на дату {request.check_in_date.strftime('%d.%m.%Y')} свободных номеров нет.")

    return booked_rooms_by_date

def calculate_revenue(booked_rooms_by_date, rooms):
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
    total_revenue, missed_revenue, empty_rooms = calculate_revenue(booked_rooms_by_date, rooms)
    total_rooms = len(rooms)
    print('\n')
    print(f"Отчет за {current_date.strftime('%d.%m.%Y')}:")
    print(f"Количество занятых номеров: {total_rooms - empty_rooms}")
    print(f"Количество свободных номеров: {empty_rooms}")
    print("Процент загруженности отдельных категорий номеров:")

    for room_type in set([room.room_type for room in rooms]):
        if current_date in booked_rooms_by_date.keys():
            occupied_rooms = sum([1 for room in rooms if room.room_type == room_type and room.number in booked_rooms_by_date[current_date]])
        else:
            occupied_rooms = 0
        total_rooms_type = sum([1 for room in rooms if room.room_type == room_type])

        print(f"{room_type}: {round(occupied_rooms / total_rooms_type * 100, 2)}%")
    print(f"Процент загруженности гостиницы в целом: {round((total_rooms - empty_rooms) / total_rooms * 100, 2)}%")
    print(f"Полученный доход за день: {total_revenue} руб.")
    print(f"Упущенный доход: {missed_revenue} руб.")
    print('\n')
def main():

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
        print(len(order))
        print_report(process_booking_requests(rooms, order, datetime(2020, 3, day)), rooms, current_date)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()