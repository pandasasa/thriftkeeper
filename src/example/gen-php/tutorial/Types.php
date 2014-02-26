<?php
namespace tutorial;

/**
 * Autogenerated by Thrift Compiler (0.9.1)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
use Thrift\Base\TBase;
use Thrift\Type\TType;
use Thrift\Type\TMessageType;
use Thrift\Exception\TException;
use Thrift\Exception\TProtocolException;
use Thrift\Protocol\TProtocol;
use Thrift\Protocol\TBinaryProtocolAccelerated;
use Thrift\Exception\TApplicationException;


final class Operation {
  const ADD = 1;
  const SUBTRACT = 2;
  const MULTIPLY = 3;
  const DIVIDE = 4;
  static public $__names = array(
    1 => 'ADD',
    2 => 'SUBTRACT',
    3 => 'MULTIPLY',
    4 => 'DIVIDE',
  );
}

class Work extends TBase {
  static $_TSPEC;

  public $num1 = 0;
  public $num2 = null;
  public $op = null;
  public $comment = null;

  public function __construct($vals=null) {
    if (!isset(self::$_TSPEC)) {
      self::$_TSPEC = array(
        1 => array(
          'var' => 'num1',
          'type' => TType::I32,
          ),
        2 => array(
          'var' => 'num2',
          'type' => TType::I32,
          ),
        3 => array(
          'var' => 'op',
          'type' => TType::I32,
          ),
        4 => array(
          'var' => 'comment',
          'type' => TType::STRING,
          ),
        );
    }
    if (is_array($vals)) {
      parent::__construct(self::$_TSPEC, $vals);
    }
  }

  public function getName() {
    return 'Work';
  }

  public function read($input)
  {
    return $this->_read('Work', self::$_TSPEC, $input);
  }
  public function write($output) {
    return $this->_write('Work', self::$_TSPEC, $output);
  }
}

class InvalidOperation extends TException {
  static $_TSPEC;

  public $what = null;
  public $why = null;

  public function __construct($vals=null) {
    if (!isset(self::$_TSPEC)) {
      self::$_TSPEC = array(
        1 => array(
          'var' => 'what',
          'type' => TType::I32,
          ),
        2 => array(
          'var' => 'why',
          'type' => TType::STRING,
          ),
        );
    }
    if (is_array($vals)) {
      parent::__construct(self::$_TSPEC, $vals);
    }
  }

  public function getName() {
    return 'InvalidOperation';
  }

  public function read($input)
  {
    return $this->_read('InvalidOperation', self::$_TSPEC, $input);
  }
  public function write($output) {
    return $this->_write('InvalidOperation', self::$_TSPEC, $output);
  }
}

$GLOBALS['tutorial_CONSTANTS']['INT32CONSTANT'] = 9853;

$GLOBALS['tutorial_CONSTANTS']['MAPCONSTANT'] = array(
  "hello" => "world",
  "goodnight" => "moon",
);


