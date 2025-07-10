from rest_framework import serializers
from api.models.test_typesDB import AllTestTypes


#for getting test topics types that belong to (DTM tests, President Schools tests)
class AllTestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllTestTypes
        fields = ["id","test_type","description","image_url","link_for_test"]
