import QtQuick 2.13
import QtQuick.Controls 2.13
import QtQml.Models 2.13


DelegateModel {
    id: visualModel
    model: client && client.model

    property var parentContainer: null
    property bool itemHeld: false

    signal changeColorRequest(var itemObject)

    delegate: Component {
        id: delegateCmp

        MouseArea {
            id: dragArea
            width: dragItemRct.width
            height: dragItemRct.height
            acceptedButtons: Qt.LeftButton | Qt.RightButton

            drag.target: held ? dragItemRct : undefined
            drag.axis: Drag.XAndYAxis

            property bool held: false

            onPressAndHold: {
                held = true
                visualModel.itemHeld = true
            }

            onReleased: {
                held = false
                visualModel.itemHeld = false
            }

            onClicked: {
                if ( mouse.button == Qt.RightButton ) {
                    visualModel.changeColorRequest(dragItemRct)
                }
            }

            Rectangle {
                id: dragItemRct
                width: 100
                height: 100
                radius: 10
                color: modelData
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    verticalCenter: parent.verticalCenter
                }

                states: [
                    State {
                        when: dragArea.held
                        // to make able freely move dragged item next steps are required:
                        // 1. re-bind current item to the outer container, i.e. GridView
                        ParentChange { target: dragItemRct; parent: visualModel.parentContainer }
                        // 2. in addition to unbind reset anchoring to the MouseArea
                        AnchorChanges {
                            target: dragItemRct
                            anchors { horizontalCenter: undefined; verticalCenter: undefined }
                        }
                        PropertyChanges { target: dragItemRct; scale: 0.5 }
                    }
                ]

                Behavior on scale { NumberAnimation{ duration: 100 } }

                Drag.active: dragArea.held
                Drag.source: dragArea
                Drag.hotSpot.x: width / 2
                Drag.hotSpot.y: height / 2
            }

            DropArea {
                anchors { fill: parent; margins: 20 }

                onEntered: {
                    visualModel.items.move(drag.source.DelegateModel.itemsIndex, dragArea.DelegateModel.itemsIndex)
                }
            }

            SequentialAnimation {
                id: shakeAnim
                loops: Animation.Infinite
                // shake only items that are not currently dragged
                running: visualModel.itemHeld && !dragArea.held

                RotationAnimation {
                    target: dragItemRct
                    to: 3
                    duration: 120
                }
                RotationAnimation {
                    target: dragItemRct
                    to: -3
                    duration: 120
                }

                onRunningChanged: {
                    if ( !running ) {
                        dragItemRct.rotation = 0
                    }
                }
            }
        }
    }
}