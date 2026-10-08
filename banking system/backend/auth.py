from routes.user import User


def check_card_number(card_number):
	number = str(card_number).strip()
	if len(number) != 6 or not number.isdigit():
		return False

	return find_user_by_card_number(number) is not None


def find_user_by_card_number(card_number):
	number = str(card_number).strip()
	if len(number) != 6 or not number.isdigit():
		return None

	return next(
		(
			user
			for user in User.load_users()
			if str(user.get("card_number")) == number
		),
		None,
	)

