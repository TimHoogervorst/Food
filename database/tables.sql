/*
CREATE TABLES FOR POSTGRESS DATABASE
*/

CREATE TABLE development."recipes" (
  "id" VARCHAR PRIMARY KEY,
  "title" VARCHAR,
  "description" VARCHAR,
  "cuisine" VARCHAR,
  "category" VARCHAR,
  "servings" integer,
  "prep time" integer,
  "cook time" integer,
  "difficulty" integer
);

CREATE TABLE development."ingredients" (
  "id" VARCHAR PRIMARY KEY,
  "fdcId" VARCHAR,
  "description" VARCHAR,
  "dataType" VARCHAR,
  "brandOwner" VARCHAR,
  "marketCountry" VARCHAR,
  "modifiedDate" TIMESTAMPTZ,
  "foodCategory" VARCHAR,
  "dataSource" VARCHAR,
  "servingSizeUnit" VARCHAR,
  "servingSize" decimal,
  "score" decimal,
  "microbes" VARCHAR,
  "foodAttributes" VARCHAR,
  "foodMeasures" VARCHAR
);

CREATE TABLE development."mix" (
  "id" VARCHAR PRIMARY KEY,
  "recipe_id" VARCHAR,
  "ingredient_id" VARCHAR,
  CONSTRAINT "FK_mix.recipe_id"
    FOREIGN KEY ("recipe_id")
      REFERENCES development.recipes("id"),
  CONSTRAINT "FK_mix.ingredient_id"
    FOREIGN KEY ("ingredient_id")
      REFERENCES development.ingredients("id")
);

CREATE TABLE development."nutrients" (
  "id" VARCHAR PRIMARY KEY,
  "ingredient_id" VARCHAR,
  "nutrientId" integer,
  "nutrientName" VARCHAR,
  "nutrientNumber" integer,
  "unitName" VARCHAR,
  "value" decimal,
  "rank" integer,
  "percentDailyValue" decimal,
  CONSTRAINT "FK_nutrients.ingredient_id"
    FOREIGN KEY ("ingredient_id")
      REFERENCES development.ingredients("id")
);

