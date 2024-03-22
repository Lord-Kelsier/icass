from time import sleep
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from src.Models import Base, Hormiga, Hormiguero, HormigaHormigueroAssociation
from src.Models import Comida, Roles, Estados, Huevo

class Simulator:
  def __init__(self):
    sleep(10) # wait for db initialization
    self.engine = create_engine(r"postgresql+psycopg2://postgres:RandomPassword@db:5432/postgres")
    Base.metadata.create_all(self.engine)
    self.session = sessionmaker(self.engine)
    with  self.session() as session:
      nest = Hormiguero(
        reina = None,
        agua = 0,
        comida = Comida(
        comidaObrera = 100,
        comidaSoldado = 100,
        comidaRealeza = 100,
        comidaNodriza = 100,
        comidaSepulturera = 100
      ))
      queen = Hormiga(
        salud = 100,
        fuerza = 100,
        velocidad = 100,
        rol = Roles.Reina,
        estado = Estados.nada,
        hormiguero = nest
      )     
      nest.hormigas.append(queen)
      nest.reina = queen.id
      session.add(nest)
      session.commit()

  def layEggs(self, queen: Hormiga, session):
    egg = Huevo(
      fechaPuesta = datetime.now(),
      hormiguero = queen.hormiguero,
      salud = 100
    )
    session.add(egg)

  def step(self):
    query = select(Hormiga).where(Hormiga.id == 1)
    with self.session() as session:
      result = list(session.execute(query).scalars())
      if len(result) != 1:
        raise RuntimeError("No se encontro la hormiga reina")
      queen = result[0]
      self.layEggs(queen, session)
      session.commit()
