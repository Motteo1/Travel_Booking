"""create test cases for all methods in engine.py"""
#         Base.metadata.create_all(self.__engine)
#         Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
#         self.__session = Session()
#
#     def close(self):
#         """close session"""
#         self.__session.close()
#
#     def get(self, cls, id):
#         """get object by id"""
#         if cls and id:
#             key = cls + '.' + id
#             if key in self.__objects:
#                 return self.__objects[key]
#         return None
#
#     def count(self, cls=None):
#         """count number of objects in storage"""
#         if cls:
#             return len(self.all(cls))
#         return len(self.all())
#