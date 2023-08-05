/****************************************************************************
**
** Copyright (C) 2019 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of Qt Quick 3D.
**
** $QT_BEGIN_LICENSE:GPL$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 or (at your option) any later version
** approved by the KDE Free Qt Foundation. The licenses are as published by
** the Free Software Foundation and appearing in the file LICENSE.GPL3
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
** $QT_END_LICENSE$
**
****************************************************************************/

import QtQuick 2.15
import HelperWidgets 2.0
import QtQuick.Layouts 1.12

Column {
    width: parent.width
    Section {
        caption: qsTr("Scene Environment")
        width: parent.width
        SectionLayout {
            Label {
                text: qsTr("Antialiasing Mode")
                tooltip: qsTr("Sets the antialiasing mode applied to the scene.")
            }
            SecondColumnLayout {
                ComboBox {
                    scope: "SceneEnvironment"
                    model: ["NoAA", "SSAA", "MSAA", "ProgressiveAA"]
                    backendValue: backendValues.antialiasingMode
                    Layout.fillWidth: true
                }
            }
            Label {
                text: qsTr("Antialiasing Quality")
                tooltip: qsTr("Sets the level of antialiasing applied to the scene.")
            }
            SecondColumnLayout {
                ComboBox {
                    scope: "SceneEnvironment"
                    model: ["Medium", "High", "VeryHigh"]
                    backendValue: backendValues.antialiasingQuality
                    Layout.fillWidth: true
                }
            }
            Label {
                text: qsTr("Temporal AA")
                tooltip: qsTr("Enables temporal antialiasing using camera jittering and frame blending.")
            }
            SecondColumnLayout {
                CheckBox {
                    text: backendValues.temporalAAEnabled.valueToString
                    backendValue: backendValues.temporalAAEnabled
                    Layout.fillWidth: true
                }
            }
            Label {
                text: qsTr("Temporal AA Strength")
                tooltip: qsTr("Sets the amount of temporal antialiasing applied.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 2.0
                    minimumValue: 0.01
                    decimals: 2
                    backendValue: backendValues.temporalAAStrength
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("Background Mode")
                tooltip: qsTr("Controls if and how the background of the scene should be cleared.")
            }
            SecondColumnLayout {
                ComboBox {
                    scope: "SceneEnvironment"
                    model: ["Transparent", "Unspecified", "Color", "SkyBox"]
                    backendValue: backendValues.backgroundMode
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("Enable Depth Test")
                tooltip: qsTr("Enables depth testing. Disable to optimize render speed for layers with mostly transparent objects.")
            }
            SecondColumnLayout {
                CheckBox {
                    text: backendValues.depthTestEnabled.valueToString
                    backendValue: backendValues.depthTestEnabled
                    Layout.fillWidth: true
                }
            }
            Label {
                text: qsTr("Enable Depth Prepass")
                tooltip: qsTr("Draw depth buffer as a separate pass. Disable to optimize render speed for layers with low depth complexity.")
            }
            SecondColumnLayout {
                CheckBox {
                    text: backendValues.depthPrePassEnabled.valueToString
                    backendValue: backendValues.depthPrePassEnabled
                    Layout.fillWidth: true
                }
            }
        }
    }

    Section {
        caption: qsTr("Clear Color")
        width: parent.width
        ColorEditor {
            caption: qsTr("Clear Color")
            backendValue: backendValues.clearColor
            supportGradient: false
            Layout.fillWidth: true
        }
    }

    Section {
        caption: qsTr("Ambient Occlusion")
        width: parent.width

        SectionLayout {

            Label {
                text: qsTr("AO Strength")
                tooltip: qsTr("Sets the amount of ambient occlusion applied.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 100
                    minimumValue: 0
                    decimals: 0
                    backendValue: backendValues.aoStrength
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("AO Distance")
                tooltip: qsTr("Sets how far ambient occlusion shadows spread away from objects.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 99999
                    minimumValue: 0
                    decimals: 0
                    backendValue: backendValues.aoDistance
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("AO Softness")
                tooltip: qsTr("Sets how smooth the edges of the ambient occlusion shading are.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 50
                    minimumValue: 0
                    decimals: 0
                    backendValue: backendValues.aoSoftness
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("AO Dither")
                tooltip: qsTr("Enables scattering of the ambient occlusion shadow band edges to improve smoothness (at the risk of sometimes producing obvious patterned artifacts).")
            }
            SecondColumnLayout {
                CheckBox {
                    text: backendValues.aoDither.valueToString
                    backendValue: backendValues.aoDither
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("AO Sample Rate")
                tooltip: qsTr("Sets the ambient occlusion quality (more shades of gray) at the expense of performance.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 4
                    minimumValue: 2
                    decimals: 0
                    backendValue: backendValues.aoSampleRate
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("AO Bias")
                tooltip: qsTr("Sets the cutoff distance preventing objects from exhibiting ambient occlusion at close distances.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 999999
                    minimumValue: -999999
                    realDragRange: 5000
                    decimals: 2
                    backendValue: backendValues.aoBias
                    Layout.fillWidth: true
                }
            }
        }
    }

    Section {
        caption: qsTr("Image Based Lighting")
        width: parent.width
        SectionLayout {
            // ### lightProbe
            Label {
                text: qsTr("Probe Brightness")
                tooltip: qsTr("Sets the amount of light emitted by the light probe.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 999999
                    minimumValue: -999999
                    realDragRange: 5000
                    decimals: 0
                    backendValue: backendValues.probeBrightness
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("Fast IBL")
                tooltip: qsTr("Use a faster approximation to image-based lighting.")
            }
            SecondColumnLayout {
                CheckBox {
                    text: backendValues.aoDither.valueToString
                    backendValue: backendValues.fastIBL
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("Probe Horizon")
                tooltip: qsTr("Upper limit for horizon darkening of the light probe.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: -0.001
                    minimumValue: -1
                    decimals: 3
                    backendValue: backendValues.probeHorizon
                    Layout.fillWidth: true
                }
            }

            Label {
                text: qsTr("Probe FOV")
                tooltip: qsTr("Image source FOV for the case of using a camera-source as the IBL probe.")
            }
            SecondColumnLayout {
                SpinBox {
                    maximumValue: 180
                    minimumValue: 1.0
                    decimals: 1
                    backendValue: backendValues.probeFieldOfView
                    Layout.fillWidth: true
                }
            }
        }
    }
}
