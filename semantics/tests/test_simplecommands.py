"""
Tests simple commands for semantics and deprecates debug_semantics
"""

# Copyright (C) 2013 Taylor Turpen
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from semantics.tree import Tree
from semantics.matching import ParseMatcher
from semantics.treehandler import TreeHandler
from pipelinehost import PipelineClient
from semantics.parsing import extract_commands

import unittest

class simplecommands(unittest.TestCase):
    """    
    """
    def setUp(self):
        self.setpairs = [("go_to_dest" , "Go to the kitchen."),
                      ("neg_go_to_dest" , "Don't go to the kitchen."),
                      ("never_go_to_dest" , ""),
                      ("neg_activate_in" , "Don't activate the camera in the bathroom."),
                      ("assert_is_in_dest" , "There is a bomb in the hallway."),
                      ("cond_see_defuse" , "If you see it, defuse it."),
                      ("cond_see_save" , "If you see hostages, save them."),
                      ("assert_are_in_dest" , "Two meals are in the kitchen."),
                      ("carry_to_dest" , "Carry them to the patient rooms."),
                      ("q_where_is_bomb" , "Where is the bomb?"),
                      ("q_where_is_hostage" , "Where is the hostage?"),
                      ("assert_in_dest" , "A book is in the kitchen."),
                      ("q_is_in_hallway" , "Is the book in the hallway?"),
                      ("q_is_in_kitchen" , "Is the book in the kitchen?"),
                      ("assert_is_in" , "The hostage is also in the kitchen."),
                      ("q_what_in_kitchen" , "What is in the kitchen?"),
                      ("q_what_in_cafeteria" , "What is in the cafeteria?"),
                      ("q_what_doing" , "What are you doing?"),
                      ("q_where_you" , "Where are you?"),
                      ("activate_camera_in_and_in" , "Activate your camera in the closet and in the hallway."),
                      ("cond_in_stay" , "If you are in the hallway, stay there.")
                      #("" , "")                
                      ]
        
        self.answers = [('go_to_dest' , 'Go to the kitchen.' , ['Verb: go\nSense: meander\nArgs:\n\tVERB: (VB.2 Go)\n\tPREP: (TO.3 to)\n\tAgent: (-NPNONE-.2 *)\n\tLocation: (NN.4 kitchen)\nNegated: False\nConditioned: False'] , ['Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: go\n\tLocation: Location\n\t\tName: kitchen\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tNegation: False'] ),
                        ('neg_go_to_dest' , "Don't go to the kitchen." , ['Verb: go\nSense: meander\nArgs:\n\tVERB: (VB.2 go)\n\tPREP: (TO.3 to)\n\tAgent: (-NPNONE-.2 *)\n\tLocation: (NN.4 kitchen)\nNegated: True\nConditioned: False'] , ['Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: go\n\tLocation: Location\n\t\tName: kitchen\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tNegation: True'] ),
                        ('never_go_to_dest' , '' , [] , []),
                        ('neg_activate_in' , "Don't activate the camera in the bathroom." , ['Verb: activate\nSense: activate\nArgs:\n\tTheme: (NN.3 camera)\n\tVERB: (VB.2 activate)\n\tLocation: (NN.4 bathroom)\n\tAgent: (-NPNONE-.2 *)\nNegated: True\nConditioned: False'] , ['Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: activate\n\tTheme: Object\n\t\tName: camera\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tLocation: Location\n\t\tName: bathroom\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tNegation: True'] ),
                        ('assert_is_in_dest' , 'There is a bomb in the hallway.' , [] , []),
                        ('cond_see_defuse' , 'If you see it, defuse it.' , ['Verb: defuse\nSense: defuse\nArgs:\n\tTheme: (PRP.3 it)\n\tVERB: (VB.2 defuse)\n\tAgent: (-NPNONE-.2 *)\nNegated: False\nConditioned: True'] , ['Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: defuse\n\tTheme: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tCondition: Command: \n\t\tAgent: Object\n\t\t\tName: None\n\t\t\tQuantifier: \n\t\t\t\tDefinite: True\n\t\t\t\tType: exact\n\t\t\t\tNumber: 1\n\t\t\tDescription: []\n\t\tAction: see\n\t\tTheme: Object\n\t\t\tName: None\n\t\t\tQuantifier: \n\t\t\t\tDefinite: True\n\t\t\t\tType: exact\n\t\t\t\tNumber: 1\n\t\t\tDescription: []\n\t\tNegation: False\n\tNegation: False'] ),
                        ('cond_see_save' , 'If you see hostages, save them.' , ['Verb: save\nSense: bill\nArgs:\n\tVERB: (VB.2 save)\n\tRecipient: (PRP.3 them)\n\tAgent: (-NPNONE-.2 *)\nNegated: False\nConditioned: True'] , ['Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: save\n\tPatient:Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tCondition: Command: \n\t\tAgent: Object\n\t\t\tName: None\n\t\t\tQuantifier: \n\t\t\t\tDefinite: True\n\t\t\t\tType: exact\n\t\t\t\tNumber: 1\n\t\t\tDescription: []\n\t\tAction: see\n\t\tTheme: Object\n\t\t\tName: hostage\n\t\t\tQuantifier: \n\t\t\t\tDefinite: True\n\t\t\t\tType: exact\n\t\t\t\tNumber: 1\n\t\t\tDescription: []\n\t\tNegation: False\n\tNegation: False'] ),
                        ('assert_are_in_dest' , 'Two meals are in the kitchen.' , ['Verb: are\nSense: be\nArgs:\n\tTheme: (NNS.2 meals)\n\tVERB: (VBP.2 are)\n\tPREP: (IN.3 in)\n\tLocation: (NN.4 kitchen)\nNegated: False\nConditioned: False'] , [] ),
                        ('carry_to_dest' , 'Carry them to the patient rooms.' , ['Verb: carry\nSense: carry\nArgs:\n\tDestination: (NN.4 patient)\n\tto towards: (TO.3 to)\n\tTheme: (PRP.3 them)\n\tVERB: (VB.2 Carry)\n\tAgent: (-NPNONE-.2 *)\nNegated: False\nConditioned: False'] , ['Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: carry\n\tTheme: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tDestination: Location\n\t\tName: patient\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tNegation: False'] ),
                        ('q_where_is_bomb' , 'Where is the bomb?' , [] , []),
                        ('q_where_is_hostage' , 'Where is the hostage?' , [] , []),
                        ('assert_in_dest' , 'A book is in the kitchen.' , [] , []),
                        ('q_is_in_hallway' , 'Is the book in the hallway?' , [] , []),
                        ('q_is_in_kitchen' , 'Is the book in the kitchen?' , [] , []),
                        ('assert_is_in' , 'The hostage is also in the kitchen.' , [] , []),
                        ('q_what_in_kitchen' , 'What is in the kitchen?' , [] , []),
                        ('q_what_in_cafeteria' , 'What is in the cafeteria?' , [] , []),
                        ('q_what_doing' , 'What are you doing?' , [] , []),
                        ('q_where_you' , 'Where are you?' , [] , []),
                        ('activate_camera_in_and_in' , 'Activate your camera in the closet and in the hallway.' , ['Verb: activate\nSense: activate\nArgs:\n\tTheme: (NN.3 camera)\n\tVERB: (VB.2 Activate)\n\tLocation: (NN.4 closet)\n\tAgent: (-NPNONE-.2 *)\nNegated: False\nConditioned: False', 'Verb: activate\nSense: activate\nArgs:\n\tTheme: (NN.3 camera)\n\tVERB: (VB.2 Activate)\n\tLocation: (NN.4 hallway)\n\tAgent: (-NPNONE-.2 *)\nNegated: False\nConditioned: False'] , ['Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: activate\n\tTheme: Object\n\t\tName: camera\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tLocation: Location\n\t\tName: closet\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tNegation: False', 'Command: \n\tAgent: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tAction: activate\n\tTheme: Object\n\t\tName: camera\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tLocation: Location\n\t\tName: hallway\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tNegation: False'] ),
                        ('cond_in_stay' , 'If you are in the hallway, stay there.' , ['Verb: stay\nSense: stay\nArgs:\n\tTheme: (-NPNONE-.2 *)\n\tVERB: (VB.2 stay)\nNegated: False\nConditioned: True'] , ['Command: \n\tAction: stay\n\tTheme: Object\n\t\tName: None\n\t\tQuantifier: \n\t\t\tDefinite: True\n\t\t\tType: exact\n\t\t\tNumber: 1\n\t\tDescription: []\n\tCondition: Command: \n\t\tAction: be\n\t\tTheme: Object\n\t\t\tName: None\n\t\t\tQuantifier: \n\t\t\t\tDefinite: True\n\t\t\t\tType: exact\n\t\t\t\tNumber: 1\n\t\t\tDescription: []\n\t\tLocation: Location\n\t\t\tName: hallway\n\t\t\tQuantifier: \n\t\t\t\tDefinite: True\n\t\t\t\tType: exact\n\t\t\t\tNumber: 1\n\t\t\tDescription: []\n\t\tNegation: False\n\tNegation: False'] ),
                        ]

        self.assertEqual(len(self.setpairs),len(set(self.setpairs)))
        self.th = TreeHandler()
        self.matcher = ParseMatcher(0,2)
        #self.generate_answers()
        
    def test_sents(self):
        """Test simple frame matching and commands sentences."""
        for key, sent, frames, commands in self.answers:            
            def test_pair(testkey,testsent,trueframes, truecommands):
                tree = PipelineClient().parse(testsent)                
                new_frames, new_commands, kb_response = extract_commands(tree, verbose=True)
                new_commands = [str(command) for command in new_commands] 
                new_frames = [frame.pprint() for frame in new_frames]
                self.assertEqual(new_frames,trueframes)
                self.assertEqual(new_commands,truecommands)
            test_pair(key,sent,frames,commands)
        
    def generate_answers(self):
        res = []
        for key, sent in self.setpairs:            
            def test_pair(testkey,testsent):
                tree = PipelineClient().parse(testsent)
                new_frames, new_commands, kb_response = extract_commands(tree, verbose=True)
                new_frames = [frame.pprint() for frame in new_frames]   
                new_commands = [str(command) for command in new_commands]             
                if len(new_frames) > 0:                    
                    return "('" + key + "' , '" + testsent + "' , " + str(new_frames) + " , " + str(new_commands) + " ),"
                else:
                    return "('" + key + "' , '" + testsent + "' , " + "[] , []),"
                                                                        
            res.append(test_pair(key,sent))
        for i in res: print i
        a = input('stop')
                

        
            
if __name__=="__main__":
    unittest.main()
                
