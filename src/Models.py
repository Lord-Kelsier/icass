from __future__ import annotations
import enum
from typing import List
from sqlalchemy import ForeignKey, Integer, Enum, DateTime, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Estados(enum.Enum):
  transportando = 1
  explorando = 2
  nada = 3
  luchando = 4

class Roles(enum.Enum):
  Reina = 1
  Princesa = 2
  Principe = 3
  Nodriza = 4
  Obrera = 5
  Soldado = 6
  Sepulturera = 7

class Base(DeclarativeBase):
  pass

class HormigaHormigueroAssociation(Base):
  __tablename__ = 'AsociacionHH'
  hormiguero_id: Mapped[int] = mapped_column(ForeignKey('hormigueros.id'), primary_key=True)
  hormiga_id: Mapped[int] = mapped_column(ForeignKey('hormigas.id'), primary_key=True)
  
class Hormiguero(Base):
  __tablename__ = "hormigueros"
  __table_args__ = (UniqueConstraint('id'),)
  id: Mapped[int] = mapped_column(primary_key=True)
  reina: Mapped[int] = mapped_column(ForeignKey('hormigas.id'), nullable=True)
  comida: Mapped[Comida] = relationship(back_populates='hormiguero')
  comida_id: Mapped[int] = mapped_column(ForeignKey('comidas.id'))
  agua: Mapped[int] = mapped_column(Integer, nullable=False)
  huevos: Mapped[List[Huevo]] = relationship()
  hormigas: Mapped[List[Hormiga]] = relationship(secondary='AsociacionHH', back_populates='hormiguero')

  def __repr__(self) -> str:
    return f"Hormiguero(id={self.id!r}, comida={self.comida!r}, agua={self.agua!r})"
  
class Hormiga(Base):
  __tablename__ = "hormigas"
  __table_args__ = (UniqueConstraint('id'),)
  id: Mapped[int] = mapped_column(primary_key=True)
  salud: Mapped[int] = mapped_column(Integer)
  fuerza: Mapped[int] = mapped_column(Integer)
  velocidad: Mapped[int] = mapped_column(Integer)
  rol: Mapped[Roles] = mapped_column(Enum(Roles))
  estado: Mapped[Estados] = mapped_column(Enum(Estados))
  hormiguero: Mapped[Hormiguero] = relationship(secondary='AsociacionHH', back_populates='hormigas')

  def __repr__(self) -> str:
    return f"Hormiga(id={self.id!r}, rol={self.rol!r}, salud={self.salud!r})"

class Comida(Base):
  __tablename__ = "comidas"
  id: Mapped[int] = mapped_column(primary_key=True)
  hormiguero: Mapped[Hormiguero] = relationship(back_populates='comida')
  comidaObrera: Mapped[int] = mapped_column(Integer, nullable=False)
  comidaSoldado: Mapped[int] = mapped_column(Integer, nullable=False)
  comidaRealeza: Mapped[int] = mapped_column(Integer, nullable=False)
  comidaNodriza: Mapped[int] = mapped_column(Integer, nullable=False)
  comidaSepulturera: Mapped[int] = mapped_column(Integer, nullable=False)

  def __repr__(self) -> str:
    return f"Comida(id={self.id!r}, comidaObrera={self.comidaObrera!r}, comidaNodriza={self.comidaNodriza!r}, comidaSoldado={self.comidaSoldado!r}, comidaRealeza={self.comidaRealeza!r}, comidaSepulturera={self.comidaSepulturera!r})"

class Huevo(Base):
  __tablename__ = "huevos"
  id: Mapped[int] = mapped_column(primary_key=True)
  fechaPuesta: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
  salud: Mapped[int] = mapped_column(Integer, nullable=False)
  hormiguero_id: Mapped[int] = mapped_column(ForeignKey('hormigueros.id'))
  hormiguero: Mapped[Hormiguero] = relationship(back_populates='huevos')

  def __repr__(self) -> str:
    return f"Huevos(id={self.id!r}, fechaPuesta={self.fechaPuesta!r}, hormiguero={self.hormiguero!r}, salud={self.salud!r})"