# The PEP 484 type hints stub file for the QtSensors module.
#
# Generated by SIP 5.3.0
#
# Copyright (c) 2020 Riverbank Computing Limited <info@riverbankcomputing.com>
# 
# This file is part of PyQt5.
# 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# info@riverbankcomputing.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.


import typing
import sip

from PyQt5 import QtCore

# Support for QDate, QDateTime and QTime.
import datetime

# Convenient type aliases.
PYQT_SIGNAL = typing.Union[QtCore.pyqtSignal, QtCore.pyqtBoundSignal]
PYQT_SLOT = typing.Union[typing.Callable[..., None], QtCore.pyqtBoundSignal]


class QSensorReading(QtCore.QObject):

    def value(self, index: int) -> typing.Any: ...
    def valueCount(self) -> int: ...
    def setTimestamp(self, timestamp: int) -> None: ...
    def timestamp(self) -> int: ...


class QAccelerometerReading(QSensorReading):

    def setZ(self, z: float) -> None: ...
    def z(self) -> float: ...
    def setY(self, y: float) -> None: ...
    def y(self) -> float: ...
    def setX(self, x: float) -> None: ...
    def x(self) -> float: ...


class QSensorFilter(sip.simplewrapper):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QSensorFilter') -> None: ...

    def filter(self, reading: QSensorReading) -> bool: ...


class QAccelerometerFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QAccelerometerFilter') -> None: ...

    def filter(self, reading: QAccelerometerReading) -> bool: ...


class QSensor(QtCore.QObject):

    class AxesOrientationMode(int): ...
    FixedOrientation = ... # type: 'QSensor.AxesOrientationMode'
    AutomaticOrientation = ... # type: 'QSensor.AxesOrientationMode'
    UserOrientation = ... # type: 'QSensor.AxesOrientationMode'

    class Feature(int): ...
    Buffering = ... # type: 'QSensor.Feature'
    AlwaysOn = ... # type: 'QSensor.Feature'
    GeoValues = ... # type: 'QSensor.Feature'
    FieldOfView = ... # type: 'QSensor.Feature'
    AccelerationMode = ... # type: 'QSensor.Feature'
    SkipDuplicates = ... # type: 'QSensor.Feature'
    AxesOrientation = ... # type: 'QSensor.Feature'
    PressureSensorTemperature = ... # type: 'QSensor.Feature'

    def __init__(self, type: typing.Union[QtCore.QByteArray, bytes, bytearray], parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def bufferSizeChanged(self, bufferSize: int) -> None: ...
    def efficientBufferSizeChanged(self, efficientBufferSize: int) -> None: ...
    def maxBufferSizeChanged(self, maxBufferSize: int) -> None: ...
    def userOrientationChanged(self, userOrientation: int) -> None: ...
    def currentOrientationChanged(self, currentOrientation: int) -> None: ...
    def axesOrientationModeChanged(self, axesOrientationMode: 'QSensor.AxesOrientationMode') -> None: ...
    def skipDuplicatesChanged(self, skipDuplicates: bool) -> None: ...
    def dataRateChanged(self) -> None: ...
    def alwaysOnChanged(self) -> None: ...
    def availableSensorsChanged(self) -> None: ...
    def sensorError(self, error: int) -> None: ...
    def readingChanged(self) -> None: ...
    def activeChanged(self) -> None: ...
    def busyChanged(self) -> None: ...
    def stop(self) -> None: ...
    def start(self) -> bool: ...
    def setBufferSize(self, bufferSize: int) -> None: ...
    def bufferSize(self) -> int: ...
    def setEfficientBufferSize(self, efficientBufferSize: int) -> None: ...
    def efficientBufferSize(self) -> int: ...
    def setMaxBufferSize(self, maxBufferSize: int) -> None: ...
    def maxBufferSize(self) -> int: ...
    def setUserOrientation(self, userOrientation: int) -> None: ...
    def userOrientation(self) -> int: ...
    def setCurrentOrientation(self, currentOrientation: int) -> None: ...
    def currentOrientation(self) -> int: ...
    def setAxesOrientationMode(self, axesOrientationMode: 'QSensor.AxesOrientationMode') -> None: ...
    def axesOrientationMode(self) -> 'QSensor.AxesOrientationMode': ...
    def isFeatureSupported(self, feature: 'QSensor.Feature') -> bool: ...
    @staticmethod
    def defaultSensorForType(type: typing.Union[QtCore.QByteArray, bytes, bytearray]) -> QtCore.QByteArray: ...
    @staticmethod
    def sensorsForType(type: typing.Union[QtCore.QByteArray, bytes, bytearray]) -> typing.List[QtCore.QByteArray]: ...
    @staticmethod
    def sensorTypes() -> typing.List[QtCore.QByteArray]: ...
    def reading(self) -> QSensorReading: ...
    def filters(self) -> typing.List[QSensorFilter]: ...
    def removeFilter(self, filter: QSensorFilter) -> None: ...
    def addFilter(self, filter: QSensorFilter) -> None: ...
    def error(self) -> int: ...
    def description(self) -> str: ...
    def setOutputRange(self, index: int) -> None: ...
    def outputRange(self) -> int: ...
    def outputRanges(self) -> typing.List['qoutputrange']: ...
    def setDataRate(self, rate: int) -> None: ...
    def dataRate(self) -> int: ...
    def availableDataRates(self) -> typing.List[typing.Tuple[int, int]]: ...
    def setSkipDuplicates(self, skipDuplicates: bool) -> None: ...
    def skipDuplicates(self) -> bool: ...
    def setAlwaysOn(self, alwaysOn: bool) -> None: ...
    def isAlwaysOn(self) -> bool: ...
    def isActive(self) -> bool: ...
    def setActive(self, active: bool) -> None: ...
    def isBusy(self) -> bool: ...
    def isConnectedToBackend(self) -> bool: ...
    def connectToBackend(self) -> bool: ...
    def type(self) -> QtCore.QByteArray: ...
    def setIdentifier(self, identifier: typing.Union[QtCore.QByteArray, bytes, bytearray]) -> None: ...
    def identifier(self) -> QtCore.QByteArray: ...


class QAccelerometer(QSensor):

    class AccelerationMode(int): ...
    Combined = ... # type: 'QAccelerometer.AccelerationMode'
    Gravity = ... # type: 'QAccelerometer.AccelerationMode'
    User = ... # type: 'QAccelerometer.AccelerationMode'

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def accelerationModeChanged(self, accelerationMode: 'QAccelerometer.AccelerationMode') -> None: ...
    def reading(self) -> QAccelerometerReading: ...
    def setAccelerationMode(self, accelerationMode: 'QAccelerometer.AccelerationMode') -> None: ...
    def accelerationMode(self) -> 'QAccelerometer.AccelerationMode': ...


class QAltimeterReading(QSensorReading):

    def setAltitude(self, altitude: float) -> None: ...
    def altitude(self) -> float: ...


class QAltimeterFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QAltimeterFilter') -> None: ...

    def filter(self, reading: QAltimeterReading) -> bool: ...


class QAltimeter(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QAltimeterReading: ...


class QAmbientLightReading(QSensorReading):

    class LightLevel(int): ...
    Undefined = ... # type: 'QAmbientLightReading.LightLevel'
    Dark = ... # type: 'QAmbientLightReading.LightLevel'
    Twilight = ... # type: 'QAmbientLightReading.LightLevel'
    Light = ... # type: 'QAmbientLightReading.LightLevel'
    Bright = ... # type: 'QAmbientLightReading.LightLevel'
    Sunny = ... # type: 'QAmbientLightReading.LightLevel'

    def setLightLevel(self, lightLevel: 'QAmbientLightReading.LightLevel') -> None: ...
    def lightLevel(self) -> 'QAmbientLightReading.LightLevel': ...


class QAmbientLightFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QAmbientLightFilter') -> None: ...

    def filter(self, reading: QAmbientLightReading) -> bool: ...


class QAmbientLightSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QAmbientLightReading: ...


class QAmbientTemperatureReading(QSensorReading):

    def setTemperature(self, temperature: float) -> None: ...
    def temperature(self) -> float: ...


class QAmbientTemperatureFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QAmbientTemperatureFilter') -> None: ...

    def filter(self, reading: QAmbientTemperatureReading) -> bool: ...


class QAmbientTemperatureSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QAmbientTemperatureReading: ...


class QCompassReading(QSensorReading):

    def setCalibrationLevel(self, calibrationLevel: float) -> None: ...
    def calibrationLevel(self) -> float: ...
    def setAzimuth(self, azimuth: float) -> None: ...
    def azimuth(self) -> float: ...


class QCompassFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QCompassFilter') -> None: ...

    def filter(self, reading: QCompassReading) -> bool: ...


class QCompass(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QCompassReading: ...


class QDistanceReading(QSensorReading):

    def setDistance(self, distance: float) -> None: ...
    def distance(self) -> float: ...


class QDistanceFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QDistanceFilter') -> None: ...

    def filter(self, reading: QDistanceReading) -> bool: ...


class QDistanceSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QDistanceReading: ...


class QGyroscopeReading(QSensorReading):

    def setZ(self, z: float) -> None: ...
    def z(self) -> float: ...
    def setY(self, y: float) -> None: ...
    def y(self) -> float: ...
    def setX(self, x: float) -> None: ...
    def x(self) -> float: ...


class QGyroscopeFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QGyroscopeFilter') -> None: ...

    def filter(self, reading: QGyroscopeReading) -> bool: ...


class QGyroscope(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QGyroscopeReading: ...


class QHolsterReading(QSensorReading):

    def setHolstered(self, holstered: bool) -> None: ...
    def holstered(self) -> bool: ...


class QHolsterFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QHolsterFilter') -> None: ...

    def filter(self, reading: QHolsterReading) -> bool: ...


class QHolsterSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QHolsterReading: ...


class QHumidityReading(QSensorReading):

    def setAbsoluteHumidity(self, value: float) -> None: ...
    def absoluteHumidity(self) -> float: ...
    def setRelativeHumidity(self, percent: float) -> None: ...
    def relativeHumidity(self) -> float: ...


class QHumidityFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QHumidityFilter') -> None: ...

    def filter(self, reading: QHumidityReading) -> bool: ...


class QHumiditySensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QHumidityReading: ...


class QIRProximityReading(QSensorReading):

    def setReflectance(self, reflectance: float) -> None: ...
    def reflectance(self) -> float: ...


class QIRProximityFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QIRProximityFilter') -> None: ...

    def filter(self, reading: QIRProximityReading) -> bool: ...


class QIRProximitySensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QIRProximityReading: ...


class QLidReading(QSensorReading):

    def frontLidChanged(self, closed: bool) -> None: ...
    def backLidChanged(self, closed: bool) -> None: ...
    def setFrontLidClosed(self, closed: bool) -> None: ...
    def frontLidClosed(self) -> bool: ...
    def setBackLidClosed(self, closed: bool) -> None: ...
    def backLidClosed(self) -> bool: ...


class QLidFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QLidFilter') -> None: ...

    def filter(self, reading: QLidReading) -> bool: ...


class QLidSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QLidReading: ...


class QLightReading(QSensorReading):

    def setLux(self, lux: float) -> None: ...
    def lux(self) -> float: ...


class QLightFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QLightFilter') -> None: ...

    def filter(self, reading: QLightReading) -> bool: ...


class QLightSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def fieldOfViewChanged(self, fieldOfView: float) -> None: ...
    def setFieldOfView(self, fieldOfView: float) -> None: ...
    def fieldOfView(self) -> float: ...
    def reading(self) -> QLightReading: ...


class QMagnetometerReading(QSensorReading):

    def setCalibrationLevel(self, calibrationLevel: float) -> None: ...
    def calibrationLevel(self) -> float: ...
    def setZ(self, z: float) -> None: ...
    def z(self) -> float: ...
    def setY(self, y: float) -> None: ...
    def y(self) -> float: ...
    def setX(self, x: float) -> None: ...
    def x(self) -> float: ...


class QMagnetometerFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QMagnetometerFilter') -> None: ...

    def filter(self, reading: QMagnetometerReading) -> bool: ...


class QMagnetometer(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def returnGeoValuesChanged(self, returnGeoValues: bool) -> None: ...
    def setReturnGeoValues(self, returnGeoValues: bool) -> None: ...
    def returnGeoValues(self) -> bool: ...
    def reading(self) -> QMagnetometerReading: ...


class QOrientationReading(QSensorReading):

    class Orientation(int): ...
    Undefined = ... # type: 'QOrientationReading.Orientation'
    TopUp = ... # type: 'QOrientationReading.Orientation'
    TopDown = ... # type: 'QOrientationReading.Orientation'
    LeftUp = ... # type: 'QOrientationReading.Orientation'
    RightUp = ... # type: 'QOrientationReading.Orientation'
    FaceUp = ... # type: 'QOrientationReading.Orientation'
    FaceDown = ... # type: 'QOrientationReading.Orientation'

    def setOrientation(self, orientation: 'QOrientationReading.Orientation') -> None: ...
    def orientation(self) -> 'QOrientationReading.Orientation': ...


class QOrientationFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QOrientationFilter') -> None: ...

    def filter(self, reading: QOrientationReading) -> bool: ...


class QOrientationSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QOrientationReading: ...


class QPressureReading(QSensorReading):

    def setTemperature(self, temperature: float) -> None: ...
    def temperature(self) -> float: ...
    def setPressure(self, pressure: float) -> None: ...
    def pressure(self) -> float: ...


class QPressureFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QPressureFilter') -> None: ...

    def filter(self, reading: QPressureReading) -> bool: ...


class QPressureSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QPressureReading: ...


class QProximityReading(QSensorReading):

    def setClose(self, close: bool) -> None: ...
    def close(self) -> bool: ...


class QProximityFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QProximityFilter') -> None: ...

    def filter(self, reading: QProximityReading) -> bool: ...


class QProximitySensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def reading(self) -> QProximityReading: ...


class qoutputrange(sip.simplewrapper):

    accuracy = ... # type: float
    maximum = ... # type: float
    minimum = ... # type: float

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'qoutputrange') -> None: ...


class QTapReading(QSensorReading):

    class TapDirection(int): ...
    Undefined = ... # type: 'QTapReading.TapDirection'
    X = ... # type: 'QTapReading.TapDirection'
    Y = ... # type: 'QTapReading.TapDirection'
    Z = ... # type: 'QTapReading.TapDirection'
    X_Pos = ... # type: 'QTapReading.TapDirection'
    Y_Pos = ... # type: 'QTapReading.TapDirection'
    Z_Pos = ... # type: 'QTapReading.TapDirection'
    X_Neg = ... # type: 'QTapReading.TapDirection'
    Y_Neg = ... # type: 'QTapReading.TapDirection'
    Z_Neg = ... # type: 'QTapReading.TapDirection'
    X_Both = ... # type: 'QTapReading.TapDirection'
    Y_Both = ... # type: 'QTapReading.TapDirection'
    Z_Both = ... # type: 'QTapReading.TapDirection'

    def setDoubleTap(self, doubleTap: bool) -> None: ...
    def isDoubleTap(self) -> bool: ...
    def setTapDirection(self, tapDirection: 'QTapReading.TapDirection') -> None: ...
    def tapDirection(self) -> 'QTapReading.TapDirection': ...


class QTapFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QTapFilter') -> None: ...

    def filter(self, reading: QTapReading) -> bool: ...


class QTapSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def returnDoubleTapEventsChanged(self, returnDoubleTapEvents: bool) -> None: ...
    def setReturnDoubleTapEvents(self, returnDoubleTapEvents: bool) -> None: ...
    def returnDoubleTapEvents(self) -> bool: ...
    def reading(self) -> QTapReading: ...


class QTiltReading(QSensorReading):

    def setXRotation(self, x: float) -> None: ...
    def xRotation(self) -> float: ...
    def setYRotation(self, y: float) -> None: ...
    def yRotation(self) -> float: ...


class QTiltFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QTiltFilter') -> None: ...

    def filter(self, reading: QTiltReading) -> bool: ...


class QTiltSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def calibrate(self) -> None: ...
    def reading(self) -> QTiltReading: ...


class QRotationReading(QSensorReading):

    def setFromEuler(self, x: float, y: float, z: float) -> None: ...
    def z(self) -> float: ...
    def y(self) -> float: ...
    def x(self) -> float: ...


class QRotationFilter(QSensorFilter):

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, a0: 'QRotationFilter') -> None: ...

    def filter(self, reading: QRotationReading) -> bool: ...


class QRotationSensor(QSensor):

    def __init__(self, parent: typing.Optional[QtCore.QObject] = ...) -> None: ...

    def hasZChanged(self, hasZ: bool) -> None: ...
    def setHasZ(self, hasZ: bool) -> None: ...
    def hasZ(self) -> bool: ...
    def reading(self) -> QRotationReading: ...
