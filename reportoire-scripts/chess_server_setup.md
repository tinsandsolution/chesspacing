this is a list of things that we did on the vultr barebones server that we got to use for free because we got like $200 in credits

`sudo apt-get update && sudo apt-get -y upgrade`

python 3 should already be installed



```
apt install python3-pip
pip install stockfish
sudo apt install stockfish
pip install chess

apt install unzip
wget https://stockfishchess.org/files/stockfish_14_linux_x64_avx2.zip
unzip stockfish_14_linux_x64_avx2.zip
mv stockfish_14_linux_x64_avx2 stockfishengine
```

you're going to want to clone the git repository and then run scripts that keep running after putty closes.
```
git clone
nohup pythonScript.py > outfile
```

### Stockfish Calibration

from stockfish import Stockfish

stockfish = Stockfish("/root/stockfishengine/stockfish_14_x64_avx2")

stockfish.get_parameters()
{'Write Debug Log': 'false', 'Contempt': 0, 'Min Split Depth': 0, 'Threads': 1, 'Ponder': 'false', 'Hash': 16, 'MultiPV': 1, 'Skill Level': 20, 'Move Overhead': 30, 'Minimum Thinking Time': 20, 'Slow Mover': 80, 'UCI_Chess960': 'false', 'UCI_LimitStrength': 'false', 'UCI_Elo': 1350}

stockfish = Stockfish(parameters={"Threads":14,"Hash": 104537,"Write Debug Log": "true"})

stockfish.set_depth(40)


stockfish.set_fen_position("rnbqk2r/ppppppbp/5np1/8/2PP4/2N2N2/PP2PPPP/R1BQKB1R b KQkq - 4 4")


