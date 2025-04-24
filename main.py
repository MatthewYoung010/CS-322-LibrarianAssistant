from LibraryDatabaseMY import *
from UserDatabase import *

JohnDoe = User("John","Doe","usgovernmentoffical@usa.sucks",1000000,"an")
Ricky = User("Ricky", "Winiski", "erikwiniski@gmail.com", 1000001 ,"Passafishy")
Steve = User("Steve", "Minecraft", "minethatwood@minecraft.block", 1000002,"BlockUpExplosives")

Userdatabase = UserDatabase()


Userdatabase.createAccount(JohnDoe.firstName,JohnDoe.lastName,JohnDoe.EMail,JohnDoe.Password)
Userdatabase.createAccount(Ricky.firstName,Ricky.lastName,Ricky.EMail,Ricky.Password)
Userdatabase.createAccount(Steve.firstName,Steve.lastName,Steve.EMail,Steve.Password)

search_Result = Userdatabase.search_user("J","","","")
for row in search_Result:
    print(row)