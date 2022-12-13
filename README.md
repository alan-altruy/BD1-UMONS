<p>
    <img src="./resources/umons.png" width="150" alt="UMONS Logo">
        &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp
    <img src="./resources/umons-fs.png" width="150" alt="UMONS Logo">
</p>

# SPJRUD Translator

### Authors

- Estebane Vanduynslager
- Alan Altruy

### Guide
<ol>
    <b><u><li>First Menu</li></u></b>
      <ul>
      <li>If you want to leave the program, enter 'q'</li>
      <li>Enter the exact path of the database you want to open</li>
      <li>If you want to use an example of database, just press 'enter'</li>
      </ul>
    <br><b><u><li>Main Menu</li></u></b>
      <ul>
      <li>Enter '1' to display the list of tables present in the database as well as the Spjrud relations created</li>
      <li>Enter '2' to open the menu allowing the display of a table or a relation</li>
      <li>Enter '3' to open the menu to create a relation from a SPJRUD expression</li>
      <li>Enter '4' to display all relations created with their SPJRUD expression and their translation in SQL</li>
      <li>Enter '5' to open the menu to save a relation in the database</li>
      <li>Enter '0' to return to the First Menu</li>
      <li>Enter an SQL request allows you to display the result (of the request) in the console</li>
      </ul>
    <br><b><u><li>Show a table/relation</li></u></b>
      <h7>You only have to enter the name of the table or the relationship (respecting the case)</h7>
    <br><br><b><u><li>Create a SPJRUD expression</li></u></b>
      <ul>
        <li>First, you must enter the name you want to give to the relationship</li>
        <li>Second, you have to enter the SPJRUD expression respecting the syntax described in point 6</li>
      </ul>
    <br><b><u><li>Save a SPJRUD expression to database</li></u></b>
      <ul>
        <li>TODO</li>
      </ul>
    <br><b><u><li>Syntax for a SPJRUD expression</li></u></b>
      <ul type="square">
      <li>For SELECT: &nbsp;&nbsp; sel(<i>column</i>, <i>operator</i>, '<i>constant</i>', <i>table</i>)
      <li>For PROJECT: &nbsp;&nbsp; proj([<i>column</i>, <i>column</i>, <i>...</i> ], <i>table</i>)
      <li>For JOIN: &nbsp;&nbsp; join(<i>table</i>, <i>table</i>)
      <li>For RENAME: &nbsp;&nbsp; ren(<i>column</i>, '<i>new_name</i>', <i>table</i>)
      <li>For UNION: &nbsp;&nbsp; union(<i>table</i>, <i>table</i>)
      <li>For DIFFERENCE: &nbsp;&nbsp; diff(<i>table</i>, <i>table</i>)
      </ul>
      -------
      <ul class="list">
      <li>where <i>'constant'</i> can also be a <i>column</i> for SELECT and operator must be <, > or =
      <li>where <i>'constant'</i> and <i>'new_name'</i> must absolutely be surrounded by apostrophes
      <li>where <i>table</i> can also be a relation (SPJRUD expression) of course
      <li>the case is important for the names of the columns and the table</li>
      </ul>
</ol>

### Features

- [x] List of Tables
- [x] List of Relations
- [x] Show a table
- [x] Show a relation
- [x] Create a SPJRUD expression
- [x] List of SPJRUD expression
- [x] Execute a SPJRUD expression
- [x] Add a table into database from a SPJRUD expression (relation)
<br>Validation of SPJRUD Expression
  - [x] Select
  - [x] Project
  - [ ] Join
  - [x] Rename
  - [x] Union
  - [x] Difference



### Remarks
<ul>
    We have implemented the program using the "code with me" plugin of Intellij,
    this is why all the commits on GitHub are in the name of alan-altruy.
</ul>