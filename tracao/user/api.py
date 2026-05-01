from ninja_extra import api_controller,route
from ninja_extra.permissions import IsAuthenticated,AllowAny,IsAdminUser
from user.schemas import ProducerTransporterRegister,CooperativeRegister,ProducerList,TransporterList,CooperativeList
from user.models import TracaoUser


User = TracaoUser

@api_controller('/users',auth=None)
class UserController:
    @route.post("/producer_signup",response = ProducerList)
    def register_producer(self,user:ProducerTransporterRegister):
        user_data = user.model_dump()
        user_data['is_producer'] = True
        user_model = User.objects.create(**user_data)
        return user_model
        
    @route.post("/transporter_signup",response = TransporterList)
    def register_transporter(self,user:ProducerTransporterRegister):
        user_data = user.model_dump()
        user_data['is_transporter'] = True
        user_model = User.objects.create(**user_data)
        return user_model

    @route.post("/cooperative_signup",response = CooperativeList)
    def register_cooperative(self,user:CooperativeRegister):
        user_data = user.model_dump()
        user_data['is_cooperative_source'] = True
        user_model = User.objects.create(**user_data)
        return user_model

    @route.get("/all_producers",response = list[ProducerList])
    def get_all_producers(self):
        return User.objects.filter(is_producer=True)

    @route.get("/all_transporters",response = list[TransporterList])
    def get_all_transporters(self):
        return User.objects.filter(is_transporter=True)

    @route.get("/all_cooperatives",response = list[CooperativeList])
    def get_all_cooperatives(self):
        return User.objects.filter(is_cooperative_source=True)