__author__ = "Paul Schifferer <dm@sweetrpg.com>"
"""
encounter.py
- Encounter controller
"""


from application.models.initiative.tracked_encounter import TrackedEncounter
from application.models.initiative.encounter import Encounter, EncounterSession, EncounterParticipant
from application.models.initiative.participant import ParticipantGroup
from application.db import db
from application.models import constants as model_constants
from urllib.parse import urlparse
from datetime import datetime
from flask import current_app


class EncounterController(object):
    def __init__(self, tracked_encounter_id):
        # super().__init__(self)
        current_app.logger.info(f"Initializing encounter controller for '{tracked_encounter_id}'...")
        self.tracked_encounter_id = tracked_encounter_id

        self._tracked_encounter = TrackedEncounter.query.filter_by(id=tracked_encounter_id).first()
        self._encounter = Encounter.query.filter_by(id=self._tracked_encounter.encounter_id).first()
        self._session = EncounterSession.query.filter_by(id=self._tracked_encounter.session_id).first()
        self._group = ParticipantGroup.query.filter_by(id=self._tracked_encounter.group_id).first()

        self._participant_map = {}
        self._arranged_participants = []
        self._participant_order_counts = {}

        self._update_arranged_participants()

    def _update_arranged_participants(self):
        current_app.logger.info("Updating arranged participants.")

        self._participant_map = {}
        self._arranged_participants = []

        if len(self._session.turn_queue) == 0:
            current_app.logger.info("Turn queue for session is empty; initializing.")
            participants = EncounterParticipant.query.filter_by(encounter_id=self._encounter.id).all()

            if len(participants) > 0:
                current_app.logger.info(f"Participant list contains: {participants}")
                self._session.turn_queue = list(map(lambda p: f"participant://{p.id}", participants))
            else:
                self._session.turn_queue = []

            db.session.add(self._session)
            db.session.commit()

        for tqe in self._session.turn_queue:
            current_app.logger.debug(f"tqe: {tqe}")
            url = urlparse(tqe)
            current_app.logger.debug(f"url: {url}")
            scheme = url.scheme
            current_app.logger.debug(f"scheme: {scheme}")
            participant_id = int(url.netloc)
            current_app.logger.debug(f"participant_id: {participant_id}")
            participant = EncounterParticipant.query.filter_by(id=participant_id).first()
            if scheme == model_constants.PARTICIPANT_SCHEME and participant is not None:
                current_app.logger.info(f"Adding participant: {participant}")
                self._participant_map[participant.id] = participant
                self._arranged_participants.append(participant)

    ## API functions

    def get_start_time(self) -> datetime:
        return self._session.start_date

    def get_end_time(self) -> datetime:
        return self._session.end_date

    def get_number_of_rounds(self) -> int:
        return self._session.number_of_rounds

    def get_number_of_turns(self) -> int:
        return self._session.number_of_turns

    def get_current_participant_id(self) -> int:
        index = int(self._session.current_participant_index)
        if index is not None:
            return self._arranged_participants[index]

        return None

    def get_current_participant_index(self) -> int:
        return self._session.current_participant_index

    def get_tied_participants(self) -> list:
        dupes = filter(lambda s: len(s) > 1, self._participant_order_counts.values())
        print(dupes)
        # TODO
        return []

    def reset(self):
        current_app.logger.info("Resetting turn queue and arrangment.")

        self._session.turn_queue = []

        db.session.add(self._session)
        db.session.commit()

        self.clear_tie_breakers()

        self._update_arranged_participants()

    def refresh_participants(self):
        current_app.logger.info("Refreshing participants.")

        self._encounter = Encounter.query.filter_by(id=self._tracked_encounter.encounter_id).first()
        self._session = EncounterSession.query.filter_by(id=self._tracked_encounter.session_id).first()
        self._group = ParticipantGroup.query.filter_by(id=self._tracked_encounter.group_id).first()

    def set_turn_to(self, index: int) -> bool:
        current_app.logger.info(f"Setting turn to participant at index {index}.")

        if index >= len(self._arranged_participants):
            return False

        participant = None
        if self._session.current_participant_index is not None:
            participant = self._arranged_participants[self._session.current_participant_index]

        self._session.current_participant_index = index

        db.session.add(self._session)
        db.session.commit()

        if participant:
            # TODO: call delegate
            pass

        return True

    def clear_tie_breakers(self):
        current_app.logger.info("Clearing tie breakers.")
        self._participant_order_counts = {}

    def set_initiative(self, value: str, participant_id: int):
        current_app.logger.info(f"Setting initiative for participant {participant_id} to {value}.")
        pass

    def sort_participants(self):
        current_app.logger.info("Sorting participants.")

        self._session.turn_queue = []
        db.session.add(self._session)

        # TODO: sort by game system rules
        if self._tracked_encounter.ordering == model_constants.ENUM_ORDERING_HIGH_TO_LOW:
            self._encounter.participants.sort(key=lambda ep: ep.order, reverse=True)
        elif self._tracked_encounter.ordering == model_constants.ENUM_ORDERING_LOW_TO_HIGH:
            pass
        elif self._tracked_encounter.ordering == model_constants.ENUM_ORDERING_PCVADVERSARY:
            pass
        elif self._tracked_encounter.ordering == model_constants.ENUM_ORDERING_PLAYER_MANAGED:
            pass

        for i,ep in enumerate(self._encounter.participants):
            current_app.logger.debug(f"{i}: {ep}")
            ep.position = i
            db.session.add(ep)

        db.session.commit()

        self._update_arranged_participants()

    def index_of(self, participant: EncounterParticipant) -> int:
        current_app.logger.info(f"Getting index of participant {participant}.")

        for i,ep in enumerate(self._arranged_participants):
            if ep.id == participant.id:
                return i

        return None

    def move_participant(self, from_index: int, to_index: int):
        current_app.logger.info(f"Moving participant at index {from_index} to {to_index}.")
        pass

    def get_next_index(self) -> int:
        current_app.logger.info(f"Getting index of next participant.")

        number_of_participants = len(self._arranged_participants)
        non_removed_participants = list(filter(lambda p: model_constants.FLAG_REMOVED not in p.flags, self._arranged_participants))

        if len(non_removed_participants) == 0:
            current_app.logger.info("No non-removed participants left.")
            return None

        if self._session.current_participant_index is None:
            current_app.logger.info("Current participant index is not set; defaulting to 0.")
            self._session.current_participant_index = 0

            db.session.add(self._session)
            db.session.commit()

            return 0

        number_of_rounds = self._session.number_of_rounds
        number_of_turns = self._session.number_of_turns

        if len(non_removed_participants) == 1:
            current_app.logger.info("One non-removed participant remains.")
            first_participant = non_removed_participants[0]
            current_app.logger.debug(f"first_participant: {first_participant}")
            if first_participant in self._arranged_participants:
                current_app.logger.info("First participant is in arranged list.")
                index = self._arranged_participants.index(first_participant)
                current_app.logger.debug(f"index: {index}")

                if self.get_current_participant_index == index:
                    # TODO: call delegate 'will-end-turn'

                    current_app.logger.info("Increasing number of rounds.")
                    number_of_rounds += 1

                    # TODO: call delegate 'will-begin-turn'

                current_app.logger.info("Increasing number of turns.")
                number_of_turns += 1

                self._session.number_of_rounds = number_of_rounds
                self._session.number_of_turns = number_of_turns
                self._session.current_participant_index = index

                current_app.logger.info("Saving session.")
                db.session.add(self._session)
                db.session.commit()

                return index

        participant_index = self.get_current_participant_index() or 0
        current_app.logger.debug(f"participant_index: {participant_index}")
        if participant_index >= len(self._arranged_participants):
            current_app.logger.info(f"Participant index {participant_index} is beyond list.")
            return None
        participant = self._arranged_participants[participant_index]
        current_app.logger.debug(f"participant: {participant}")

        # TODO: call delegate 'will-end-turn'

        current_app.logger.info("Increasing number of turns.")
        number_of_turns += 1
        current_app.logger.info("Trying to find next participant.")
        while True:
            participant_index += 1
            current_app.logger.debug(f"participant_index: {participant_index}")
            if participant_index >= number_of_participants:
                current_app.logger.info("Wrapping around.")
                participant_index = 0
                number_of_rounds += 1

            participant = self._arranged_participants[participant_index]
            current_app.logger.debug(f"participant: {participant}, non_removed_participants: {non_removed_participants}")
            if participant in non_removed_participants:
                current_app.logger.info("Participant is in non-removed list.")
                self._session.current_participant_index = participant_index

                # TODO: call delegate 'will-begin-turn'

                break

        self._session.number_of_rounds = number_of_rounds
        self._session.number_of_turns = number_of_turns

        current_app.logger.info(f"Saving session.")
        db.session.add(self._session)
        db.session.commit()

        index = self.get_current_participant_index()
        current_app.logger.info(f"Returning participant index: {index}")
        return index

    def __getitem__(self, id_or_index) -> EncounterParticipant:
        current_app.logger.debug(f"__getitem__[{id_or_index}]")
        if isinstance(id_or_index, int):
            return self._arranged_participants[int(id_or_index)]

        return self._participant_map[id_or_index]
