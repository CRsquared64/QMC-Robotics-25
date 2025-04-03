class Motion:
    def __init__(self):
        pass
    # will have to adjust these to correct ways round
    def forward(self,mBoard, power):
        mBoard.motors[0].power = -power
        mBoard.motors[1].power = power

    def backwards(self,mBoard, power):
        mBoard.motors[0].power = power
        mBoard.motors[1].power = -power

    def right(self,mBoard, power):
        mBoard.motors[0].power = power
        mBoard.motors[1].power = power

    def left(self,mBoard, power):
        mBoard.motors[0].power = -power
        mBoard.motors[1].power = -power

    def stop_motors(self,mBoard):
        for m in mBoard.motors:
            m.power = 0