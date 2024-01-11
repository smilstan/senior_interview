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
            width: 75
            height: 75

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
                print(mouse.button)
                if ( mouse.button == Qt.LeftButton ) {
                    visualModel.changeColorRequest(dragItemRct)
                }
            }

            Rectangle {
                id: dragItemRct
                width: 75
                height: 75
                radius: 10
                color: modelData
                anchors {
                    horizontalCenter: parent.horizontalCenter
                    verticalCenter: parent.verticalCenter
                }

                states: [
                    State {
                        when: dragArea.held

                        ParentChange { target: dragItemRct; parent: visualModel.parentContainer }
                        AnchorChanges {
                            target: dragItemRct
                            anchors { horizontalCenter: undefined; verticalCenter: undefined }
                        }
                        PropertyChanges { target: dragItemRct; scale: 0.5 }
                    }
                ]

                Behavior on scale { NumberAnimation{ duration: 100 } }

                SequentialAnimation {
                    id: shakeAnim
                    loops: Animation.Infinite
                    running: visualModel.itemHeld && !dragArea.held

                    RotationAnimation {
                        target: dragItemRct
                        to: 5
                        duration: 100
                    }
                    RotationAnimation {
                        target: dragItemRct
                        to: -5
                        duration: 100
                    }

                    onRunningChanged: {
                        if ( !running ) {
                            dragItemRct.rotation = 0
                        }
                    }
                }

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
        }
    }
}