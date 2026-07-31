from sqlalchemy.orm import Session

# with Session(engine) as session:
#     spongebob = User(
#         name="spongebob",
#         fullname="Spongebob Squarepants",
#         addresses=[Address(email_address="spongebob@sqlalchemy.org")],
#     )
#     sandy = User(
#         name="sandy",
#         fullname="Sandy Cheeks",
#         addresses=[
#             Address(email_address="sandy@sqlalchemy.org"),
#             Address(email_address="sandy@squirrelpower.org"),
#         ],
#     )
#     patrick = User(name="patrick", fullname="Patrick Star")
#     session.add_all([spongebob, sandy, patrick])
#     session.commit()

    # expire_on_commit = False
    # sandy.name 不会获取数据库磁盘中存储的最新信息.而是会从sandy内存中获取

    # expire_on_commit = True
    # sandy.name 就过期了, 如果想要获取这个属性值,那么sandy.name会自动执行一条sql从数据库中获取最新的值