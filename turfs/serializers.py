from .models import *
w

class Turf_registration_serializers(serializers.ModelSerializer):
    class Meta:
        model = Turf_registration
        fields = '__all__'

class Forget_turf_password_serializers(serializers.ModelSerializer):
    class Meta:
        model = Forget_turf_password
        fields = '__all__'

class Random_token_seriallizer1(serializers.ModelSerializer):
    class Meta:
        model = Random_token_generation
        fields = '__all__'

class Update_turf_mobile_number_serializer1(serializers.ModelSerializer):
    class Meta:
        model = Update_turf_mobile_number
        fields = '__all__'
    