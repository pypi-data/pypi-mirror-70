#!/usr/bin/env python3

from blockapi.base_api import BaseBlockApi, DEFAULT_TIMEOUT
from blockapi.cmdid import PCProgramCmdId
from pb2.codemao_changerobotvolume_pb2 import ChangeRobotVolumeRequest, ChangeRobotVolumeResponse
from pb2.codemao_controlrobotrecord_pb2 import ControlRobotRecordRequest, ControlRobotRecordResponse
from pb2.codemao_getactionlist_pb2 import GetActionListRequest, GetActionListResponse
from pb2.codemao_moverobot_pb2 import MoveRobotRequest, MoveRobotResponse
from pb2.codemao_playaction_pb2 import PlayActionRequest, PlayActionResponse
from pb2.codemao_playcustomaction_pb2 import PlayCustomActionRequest, PlayCustomActionResponse
from pb2.codemao_stopaction_pb2 import StopActionRequest, StopActionResponse
from pb2.codemao_stopcustomaction_pb2 import StopCustomActionRequest, StopCustomActionResponse
from pb2.pccodemao_message_pb2 import Message


class PlayAction(BaseBlockApi):
    """
    执行动作
    默认串行
    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        assert action_name is not None and len(action_name), 'PlayAction actionName should be available'
        self.__isSerial = is_serial
        self.__actionName = action_name

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = PlayActionRequest()
        request.actionName = self.__actionName

        cmd_id = PCProgramCmdId.PLAY_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopAllAction(BaseBlockApi):

    def __init__(self, is_serial: bool = True):
        self.__isSerial = is_serial

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = StopActionRequest()

        cmd_id = PCProgramCmdId.STOP_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = StopActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class MoveRobot(BaseBlockApi):
    # TODO direction参数定义枚举
    def __init__(self, is_serial: bool = True, direction: int = None, step: int = None):
        assert direction is not None and direction > 0, 'direction should not be None,and should be Positive'
        assert step is not None and step > 0, 'step should not be None,and should be Positive'
        self.__isSerial = is_serial
        self.__direction = direction
        self.__step = step

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = MoveRobotRequest()
        request.direction = self.__direction
        request.step = self.__step

        cmd_id = PCProgramCmdId.MOVE_ROBOT_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = MoveRobotResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class GetActionList(BaseBlockApi):

    def __init__(self, is_serial: bool = True, language_type: str = None, action_type: int = None):
        assert language_type is not None and len(language_type) > 0, 'GetActionList languageType should be available'
        assert action_type is not None and action_type > 0, 'action_type should not be None,and should be Positive'
        self.__isSerial = is_serial
        self.__languageType = language_type
        self.__actionType = action_type

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = GetActionListRequest()
        request.languageType = self.__languageType
        request.actionType = self.__actionType

        cmd_id = PCProgramCmdId.GET_ACTION_LIST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = GetActionListResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class PlayCustomAction(BaseBlockApi):
    """
    执行自定义动作
    默认串行
    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        assert action_name is not None and len(action_name) > 0, 'PlayCustomAction actionName should be available'
        self.__isSerial = is_serial
        self.__actionName = action_name

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = PlayCustomActionRequest()
        request.actionName = self.__actionName

        cmd_id = PCProgramCmdId.PLAY_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = PlayCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class StopCustomAction(BaseBlockApi):
    """
    停止自定义动作
    默认串行
    """

    def __init__(self, is_serial: bool = True, action_name: str = None):
        assert action_name is not None and len(action_name) > 0, 'StopCustomAction actionName should be available'
        self.__isSerial = is_serial
        self.__actionName = action_name

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = StopCustomActionRequest()
        request.actionName = self.__actionName

        cmd_id = PCProgramCmdId.STOP_CUSTOM_ACTION_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = StopCustomActionResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ChangeRobotVolume(BaseBlockApi):
    """
    设置机器人音量
    volume:0-1 浮点数，默认0.0
    """

    def __init__(self, is_serial: bool = True, volume: float = 0.0):
        assert 0.0 <= volume <= 1.0, 'ChangeRobotVolume volume should be in range[0.0,1.0]'
        self.__isSerial = is_serial
        self.__volume = volume

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT

        request = ChangeRobotVolumeRequest()
        request.volume = self.__volume

        cmd_id = PCProgramCmdId.CHANGE_ROBOT_VOLUME_REQUEST.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ChangeRobotVolumeResponse()
            response.ParseFromString(data)
            return response
        else:
            return None


class ControlRobotAudioRecord(BaseBlockApi):
    """
    控制机器人录音/播放
    type: 0 -> 开始录音 1 -> 停止录音 2 -> 开始播放 3 -> 停止播放 4 -> 暂停播放 5 -> 继续播放 6 -> 重命名名字(Base64)
    timelimit:单位ms
    """

    def __init__(self, is_serial: bool = True, ptype: int = 0, time_limit: int = 0, _id: str = None,
                 new_id: str = None):
        assert ptype >= 0, 'RobotAudioRecord type should be positive'
        self.__isSerial = is_serial
        self.__type = ptype
        self.__timeLimit = time_limit
        self.__id = _id
        self.__newId = new_id

    async def execute(self):
        timeout = 0
        if self.__isSerial:
            timeout = DEFAULT_TIMEOUT
        request = ControlRobotRecordRequest()
        request.type = self.__type
        request.timeLimit = self.__timeLimit
        request.id = self.__id
        request.newId = self.__newId

        cmd_id = PCProgramCmdId.CONTROL_ROBOT_AUDIO_RECORD.value
        return await self.send(cmd_id, request, timeout)

    def parse_msg(self, message):
        if isinstance(message, Message):
            data = message.bodyData
            response = ControlRobotRecordResponse()
            response.ParseFromString(data)
            return response
        else:
            return None
