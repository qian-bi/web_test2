from .dbSession import Base, engine


def run():
    print('------------create_all-------------')
    Base.metadata.create_all(engine)
    print('------------create_end-------------')


if __name__ == "__main__":
    run()
