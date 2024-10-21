from pyteal import *
import json

def approval_program():
    MAX_EVENTS = Int(5)
    EVENT_COUNT = Bytes("event_count")
    EVENT_NFT_PREFIX = Bytes("event_")
    NFT_ID_SUFFIX = Bytes("_nft_id")
    EVENT_END_PREFIX = Bytes("event_end_")
    EVENT_STOPPED_PREFIX = Bytes("event_stopped_")

    # Helper function to convert integer to its ASCII byte representation
    def int_to_str(i):
        return If(
            i == Int(1),
            Bytes("1"),
            If(
                i == Int(2),
                Bytes("2"),
                If(
                    i == Int(3),
                    Bytes("3"),
                    If(
                        i == Int(4),
                        Bytes("4"),
                        If(
                            i == Int(5),
                            Bytes("5"),
                            Bytes("")  # Fallback, should not happen due to MAX_EVENTS
                        )
                    )
                )
            )
        )

    # On Creation: Initialize event_count to 0
    on_creation = Seq([
        Log(Bytes("Creating contract, initializing event_count to 0")),
        App.globalPut(EVENT_COUNT, Int(0)),
        Return(Int(1))
    ])

    # Conditions to handle create_event
    create_event = And(
        Txn.application_args.length() == Int(3),
        Txn.application_args[0] == Bytes("create_event"),
        Txn.sender() == Global.creator_address()
    )

    handle_create_event = Seq([
        Log(Bytes("Handling create_event")),
        # Kiểm tra không vượt quá MAX_EVENTS
        Assert(App.globalGet(EVENT_COUNT) < MAX_EVENTS),
        Log(Bytes("Event count is within limit")),
        # Tăng event_count
        App.globalPut(EVENT_COUNT, App.globalGet(EVENT_COUNT) + Int(1)),
        Log(Bytes("Incremented event_count")),
        # Lưu nft_id vào global state với key tương ứng
        App.globalPut(
            Concat(
                EVENT_NFT_PREFIX,
                int_to_str(App.globalGet(EVENT_COUNT)),
                NFT_ID_SUFFIX
            ),
            Btoi(Txn.application_args[1])
        ),
        Log(Bytes("Stored nft_id")),
        # Lưu end_timestamp vào global state với key tương ứng
        App.globalPut(
            Concat(
                EVENT_END_PREFIX,
                int_to_str(App.globalGet(EVENT_COUNT))
            ),
            Btoi(Txn.application_args[2])
        ),
        Log(Bytes("Stored end_timestamp")),
        # Lưu trạng thái stopped vào global state với key tương ứng
        App.globalPut(
            Concat(
                EVENT_STOPPED_PREFIX,
                int_to_str(App.globalGet(EVENT_COUNT))
            ),
            Int(0)
        ),
        Log(Bytes("Initialized event_stopped to 0")),
        Return(Int(1))
    ])

    # Conditions to handle stop_event
    stop_event = And(
        Txn.application_args.length() == Int(2),
        Txn.application_args[0] == Bytes("stop_event"),
        Txn.sender() == Global.creator_address()
    )

    # Handle stop_event
    handle_stop_event = Seq([
        Log(Bytes("Handling stop_event")),
        Assert(Btoi(Txn.application_args[1]) <= App.globalGet(EVENT_COUNT)),
        Log(Bytes("Event ID is valid")),
        Assert(Global.latest_timestamp() >= App.globalGet(
            Concat(EVENT_END_PREFIX, int_to_str(Btoi(Txn.application_args[1]))))),
        Log(Bytes("Event has reached its end time")),
        App.globalPut(
            Concat(EVENT_STOPPED_PREFIX, int_to_str(Btoi(Txn.application_args[1]))),
            Int(1)
        ),
        Log(Bytes("Event has been stopped")),
        Return(Int(1))
    ])

    # Main program logic
    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [create_event, handle_create_event],
        [stop_event, handle_stop_event],
        [Txn.on_completion() == OnComplete.NoOp, Return(Int(1))],
        [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
        [Txn.on_completion() == OnComplete.ClearState, Return(Int(1))],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(Int(0))],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Int(0))]
    )

    return program

def clear_state_program():
    return Return(Int(1))

if __name__ == "__main__":
    from pyteal import compileTeal, Mode

    # Biên dịch và lưu approval program
    with open("approval.teal", "w") as f:
        compiled_approval = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled_approval)

    # Biên dịch và lưu clear state program
    with open("clear_state.teal", "w") as f:
        compiled_clear_state = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled_clear_state)

    # Tạo file app spec JSON theo chuẩn ARC-4
    app_spec = {
        "schema_version": 1,
        "name": "NFTicket",
        "description": "Smart contract for managing events with NFT integration.",
        "app_id": 0,  
        "creator": "MV7HWZVFW64CK2A5JCUEXXWORNZRIRQLPPNAUPO4IP4AHMZ7XB6BU2ZSNM",
        "approval_program": "approval.teal",
        "clear_state_program": "clear_state.teal",
        "global_state": {
            "schema": {
            "num_uints": 16,
            "num_byte_slices": 0
            },
            "defaults": [
            {
                "name": "event_count",
                "type": "uint64",
                "description": "The number of events created",
                "default_value": 0
            },
            # Các mục khác trong global_state...
            ]
        },
        "local_state": {
            "schema": {
            "num_uints": 0,
            "num_byte_slices": 0
            }
        },
        "methods": [
            {
            "name": "create_event",
            "args": [
                {
                "type": "uint64",
                "name": "nft_id",
                "description": "ID of the NFT associated with the event"
                },
                {
                "type": "uint64",
                "name": "end_timestamp",
                "description": "Timestamp when the event ends"
                }
            ],
            "returns": {
                "type": "uint64",
                "description": "Returns 1 on success, 0 on failure"
            },
            "description": "Create a new event with an associated NFT ID and end timestamp."
            },
            {
            "name": "stop_event",
            "args": [
                {
                "type": "uint64",
                "name": "event_id",
                "description": "The ID of the event to stop"
                }
            ],
            "returns": {
                "type": "uint64",
                "description": "Returns 1 on success, 0 on failure"
            },
            "description": "Stop an event after its end timestamp has passed."
            }
        ]
    }

    # Xuất ra file JSON
    with open("application.json", "w") as json_file:
        json.dump(app_spec, json_file, indent=4)