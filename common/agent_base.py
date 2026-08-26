class agent_base:
    def __init__(self,name):
        self.name = name

        self.actions_total_num = 0
        self.actions_invalid_num = 0
        self.invalid_action_dict = {}

    def act(self, obs):
        raise NotImplementedError(self.name+" must implement act()")

    def clear_level_cache(self):
        raise NotImplementedError(self.name + " must implement clear_level_cache()")

    def record_step_data(self, path, obs, counter):
        raise NotImplementedError(self.name + " must implement clear_level_cache()")

    def _stat_action_invalid_rate(self, obs):
        #self.actions_total_num = self.actions_total_num + 1
        if obs["text"]['Agent_Last_Action_Info']['Action_Index'] !=6:
            self.actions_total_num = self.actions_total_num + 1
            if obs["text"]['Agent_Last_Action_Info']['Error_Code']>0:
                self.actions_invalid_num = self.actions_invalid_num + 1
                if str(obs["text"]['Agent_Last_Action_Info']['Error_Code']) in self.invalid_action_dict:
                    self.invalid_action_dict[str(obs["text"]['Agent_Last_Action_Info']['Error_Code'])]+=1
                else:
                    self.invalid_action_dict[str(obs["text"]['Agent_Last_Action_Info']['Error_Code'])]=1


    def get_actions_invalid_rate(self):
        if self.actions_total_num==0:
            print("Error: action total number should not be 0")
            return 0
        return float(self.actions_invalid_num)/float(self.actions_total_num)

    def get_invalid_action_dict(self):
        return self.invalid_action_dict