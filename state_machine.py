class StateMachine:
    def __init__(self, cur_state, rules):
        self.cur_state = cur_state
        self.next_state = None
        self.rules = rules
        self.cur_state.enter(('START', None))

    def update(self):
        self.cur_state.do()

    def handle_state_event(self, state_event):
        for check_event in self.rules[self.cur_state].keys():
            if check_event(state_event):
                self.next_state = self.rules[self.cur_state][check_event]
                if not self.cur_state.exit(state_event): continue
                self.next_state.enter(state_event)
                # print(f'{self.cur_state.__class__.__name__} - {state_event[0]} -> {self.next_state.__class__.__name__}')
                self.cur_state = self.next_state
                return

    def draw(self):
        self.cur_state.draw()