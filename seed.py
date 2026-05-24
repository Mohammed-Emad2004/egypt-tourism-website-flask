from app import app
from app.models import db, Place, PlaceTranslation
from app.data import places_raw_data
from app.models import User
from werkzeug.security import generate_password_hash

def seed_database():
    with app.app_context():
        db.create_all()

        if Place.query.first():
            print("Database already seeded.")
            return

        print("The data is being inserted into MySQL...")

        for p_data in places_raw_data:
            new_place = Place(
                id=p_data['id'],
                image_file=p_data['image_file'],
                rating=p_data['rating'],
                booking_url=p_data.get('booking_url'),
                location_url=p_data.get('location_url')
            )
            db.session.add(new_place)

            for lang, trans_data in p_data['translations'].items():
                new_trans = PlaceTranslation(
                    place_id=p_data['id'],
                    language_code=lang,
                    name=trans_data['name'],
                    category=trans_data['category'],
                    hook=trans_data.get('hook', ''),
                    description=trans_data['description'],
                    city=trans_data['city'],
                    best_time=trans_data['best_time'],
                    transportation=trans_data['transportation'],
                    activities=trans_data['activities']
                )
                db.session.add(new_trans)

        admin = User.query.filter_by(email="admin@egypttourism.com").first()

        if not admin:
            admin = User(
                username="admin",
                email="admin@egypttourism.com",
                password_hash=generate_password_hash("Admin@123"),
                country="EG",
                role="admin"
            )
            db.session.add(admin)

        db.session.commit()
        print("The data has been successfully inserted into the database!")

if __name__ == '__main__':
    seed_database()