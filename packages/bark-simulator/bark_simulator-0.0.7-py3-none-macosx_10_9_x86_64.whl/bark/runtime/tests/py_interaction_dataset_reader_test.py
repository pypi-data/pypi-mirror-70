# Copyright (c) 2020 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
from bark.runtime.scenario.interaction_dataset_processing.interaction_dataset_reader import agent_from_trackfile
from bark.runtime.commons.parameters import ParameterServer
import os

class InteractionDatasetReaderTest(unittest.TestCase):
  #@unittest.skip
  def test_agent_from_trackfile(self):

    track_ids = [1, 2, 3]

    params = ParameterServer()
    params_id = params["Scenario"]["Generation"]["InteractionDataset"]
    params_id["MapFilename", "", os.path.join(os.path.dirname(__file__),"data/DR_DEU_Merging_MT_v01_shifted.xodr")]
    params_id["TrackFilename", "", os.path.join(os.path.dirname(__file__),"data/interaction_dataset_dummy_track.csv")]
    params_id["TrackIds", "", track_ids]
    params_id["StartTs", "", 100]
    params_id["EndTs", "", None]
    params_id["EgoTrackId", "", -1]
    params_id["BehaviorModel", "", {}]

    track_params = ParameterServer()
    track_params["filename"] = params["Scenario"]["Generation"]["InteractionDataset"]["TrackFilename"]
    track_params["execution_model"] = 'ExecutionModelInterpolate'
    track_params["dynamic_model"] = 'SingleTrackModel'
    track_params["map_interface"] = None # world.map
    track_params["start_offset"] = params["Scenario"]["Generation"]["InteractionDataset"]["StartTs"]
    track_params["end_offset"] = params["Scenario"]["Generation"]["InteractionDataset"]["EndTs"]
    track_params["behavior_model"] = None

    agent_list = []
    for track_id in track_ids:
      track_params["track_id"] = track_id 
      agent = agent_from_trackfile(track_params, params, 1)
      agent_list.append(agent)
      print(agent.behavior_model)
      
    assert(len(agent_list) == len(track_ids))








if __name__ == '__main__':
  unittest.main()


