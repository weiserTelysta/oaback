from rest_framework import serializers
from rest_framework.exceptions import ValidationError, APIException, AuthenticationFailed

from apps.absent.models import Absent, AbsentType, AbsentStatusChoices
from apps.oaauth.serializers import UserSerializer
from .utils import get_responder


class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'


class AbsentSerializer(serializers.ModelSerializer):
    absent_type = AbsentTypeSerializer(read_only=True)
    absent_type_id = serializers.IntegerField(write_only=True)
    requester = UserSerializer(read_only=True)
    responder = UserSerializer(read_only=True)

    class Meta:
        model = Absent
        fields = '__all__'

    def validate_absent_type_id(self, value):
        if not AbsentType.objects.filter(pk=value).exists():
            raise ValidationError("考勤类型不存在")
        return value

    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        # 获取审批者
        responder = get_responder(request)

        if responder is None:
            validated_data['status'] = AbsentStatusChoices.PASS
        else:
            validated_data['status'] = AbsentStatusChoices.AUDITING
        absent = Absent.objects.create(**validated_data, requester=user, responder=responder)
        return absent

    def update(self, instance, validated_data):
        if instance.status != AbsentStatusChoices.AUDITING:
            raise APIException(detail='不能修改已经确定的数据')

        request = self.context['request']
        user = request.user
        responder = get_responder(request)

        if instance.responder.uid != user.uid:
            raise AuthenticationFailed(detail="您无权处理该考勤")
        instance.status = validated_data['status']

        instance.save()
        return instance
