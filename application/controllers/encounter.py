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


class EncounterController(object):
    def __init__(self, tracked_encounter_id):
        super().__init__(self)
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
        self._participant_map = {}
        self._arranged_participants = []

        if len(self._session.turn_queue) == 0:
            participants = EncounterParticipant.query.filter_by(encounter_id=self._encounter.id).all()

            if len(participants) > 0:
                self._session.turn_queue = map(lambda p: f"participant://{p.id}", participants)

                db.session.add(self._session)
                db.session.commit()

        for tqe in self._session.turn_queue:
            url = urlparse(tqe)
            scheme = url.scheme
            id = url.path
            participant = EncounterParticipant.query.filter_by(id=id).first()
            if scheme == model_constants.PARTICIPANT_SCHEME and participant is not None:
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
        self._session.turn_queue = []

        db.session.add(self._session)
        db.session.commit()

        self.clear_tie_breakers()

        self._update_arranged_participants()

    def refresh_participants(self):

        self._encounter = Encounter.query.filter_by(id=self._tracked_encounter.encounter_id).first()
        self._session = EncounterSession.query.filter_by(id=self._tracked_encounter.session_id).first()
        self._group = ParticipantGroup.query.filter_by(id=self._tracked_encounter.group_id).first()

    def set_turn_to(self, index: int) -> bool:

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
        self._participant_order_counts = {}

    def set_initiative(self, value: str, participant_id: int):
        pass

    def sort_participants(self):
        pass

    def index_of(self, participant: EncounterParticipant) -> int:
        for i,ep in enumerate(self._arranged_participants):
            if ep.id == participant.id:
                return i

        return None

    def move_participant(self, from_index: int, to_index: int):
        pass

    def get_next_index(self) -> int:

        number_of_participants = len(self._arranged_participants)
        non_removed_participants = map(lambda p: model_constants.FLAG_REMOVED in p.flags, self._arranged_participants)

        if len(non_removed_participants) == 0:
            return None

        if self._session.current_participant_index is None:
            self._session.current_participant_index = 0

            db.session.add(self._session)
            db.session.commit()

            return 0

        number_of_rounds = self._session.number_of_rounds
        number_of_turns = self._session.number_of_turns

        if len(non_removed_participants) == 1:
            first_participant = non_removed_participants[0]
            if first_participant in self._arranged_participants:
                index = self._arranged_participants.index(first_participant)

                if self.get_current_participant_index == index:
                    # TODO: call delegate 'will-end-turn'

                    number_of_rounds += 1

                    # TODO: call delegate 'will-begin-turn'

                number_of_turns += 1

                self._session.number_of_rounds = number_of_rounds
                self._session.number_of_turns = number_of_turns
                self._session.current_participant_index = index

                db.session.add(self._session)
                db.session.commit()

                return index

        participant_index = self.get_current_participant_index or 0
        if participant_index >= len(self._arranged_participants):
            return None
        participant = self._arranged_participants[participant_index]

        # TODO: call delegate 'will-end-turn'

        number_of_turns += 1
        while True:
            participant_index += 1
            if participant_index >= number_of_participants:
                participant_index = 0
                number_of_rounds += 1

            participant = self._arranged_participants[participant_index]
            if participant in non_removed_participants:
                self._session.current_participant_index = participant_index

                # TODO: call delegate 'will-begin-turn'

                break

        self._session.number_of_rounds = number_of_rounds
        self._session.number_of_turns = number_of_turns

        db.session.add(self._session)
        db.session.commit()

        return self.get_current_participant_index

    def __get_item__(self, id_or_index) -> EncounterParticipant:
        if isinstance(id_or_index, int):
            return self._arranged_participants[int(id_or_index)]

        return self._participant_map[id_or_index]
