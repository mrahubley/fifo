
from .database import Base
from sqlalchemy import Column, Boolean, Integer, String, Numeric, ForeignKey, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, index=True, unique=True, nullable=False)
    number = Column(Numeric, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(String, index=True, nullable=False)
    estimated_budget = Column(Float, index=True, nullable=False)
    is_paid = Column(Boolean, default=False, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Skills(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    description = Column(String, index=True, nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    firstname = Column(String, index=True, nullable=False)
    lastname = Column(String, index=True, nullable=False)
    gender = Column(String, index=True, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), index=True, nullable=True)
    region = Column(String, index=True, nullable=True)
    city = Column(String, index=True, nullable=True)
    town = Column(String, index=True, nullable=True)
    street = Column(String, index=True, nullable=True)
    dob = Column(String, index=True, nullable=True)
    short_info = Column(String, index=True, nullable=True)
    short_note = Column(String, index=True, nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class ProfileSkills(Base):
    __tablename__ = "profileskills"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), index=True, nullable=False)
    school_name = Column(String, index=True, nullable=False)
    degree_id = Column(Integer, ForeignKey("degrees.id", ondelete="CASCADE"), index=True, nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), index=True, nullable=False)
    start_year = Column(Integer, index=True, nullable=False)
    end_year = Column(Integer, index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class JobSkills(Base):
    __tablename__ = "jobskills"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False)
    job_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    zipcode = Column(Integer, index=True, nullable=True)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class University(Base):
    __tablename__ = "universities"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    country_id = Column(Integer, ForeignKey("countries.id", ondelete="CASCADE"), index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Degree(Base):
    __tablename__ = "degrees"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True, unique=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

class Qualification(Base):
    __tablename__ = "qualifications"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    certificate = Column(String, index=True, nullable=False)
    organization = Column(String, index=True, nullable=False)
    summary = Column(String, index=True, nullable=False)
    start_year = Column(Integer, index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id", ondelete="CASCADE"), index=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)