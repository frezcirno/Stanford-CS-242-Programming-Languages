/***************
 * NOTE:
 *   You can call `internal_login` simply by `internal_login(id, pw)`.
 ***************/

#[allow(unused_imports)]
use crate::prob1::server::internal_login;

// TODO: Implement the following typestate structs. You are free to add any fields to the struct
// definitions.
// Below shows the signature of the methods to be implemented across the cart state machine.
// Note that not all methods may be implemented for every typestate struct.
//
//   pub fn login(_: String, _: String) -> Result<T,()>
//   pub fn add_item(self, _: u32) -> T
//   pub fn clear_items(self) -> T
//   pub fn checkout(self) -> T
//   pub fn cancel(self) -> T
//   pub fn order(self) -> T
//   pub fn acct_num(&self) -> u32
//   pub fn tot_cost(&self) -> u32
//
// Here T denotes a type. Note that each T can be a different type.
//===== BEGIN_CODE =====//
pub struct Cart {}

impl Cart {
    pub fn login(id: String, pw: String) -> Result<Empty, ()> {
        match internal_login(id, pw) {
            Some(acct_num) => Ok(Empty {
                acct_num,
                tot_cost: 0,
            }),
            None => Err(()),
        }
    }
}

pub struct Empty {
    acct_num: u32,
    tot_cost: u32,
}

impl Empty {
    pub fn add_item(self, item: u32) -> NonEmpty {
        NonEmpty {
            acct_num: self.acct_num,
            items: vec![item],
        }
    }

    pub fn acct_num(&self) -> u32 {
        self.acct_num
    }

    pub fn tot_cost(&self) -> u32 {
        self.tot_cost
    }
}

pub struct NonEmpty {
    acct_num: u32,
    items: Vec<u32>,
}

impl NonEmpty {
    pub fn add_item(mut self, item: u32) -> NonEmpty {
        self.items.push(item);
        self
    }

    pub fn clear_items(self) -> Empty {
        Empty {
            acct_num: self.acct_num,
            tot_cost: 0,
        }
    }

    pub fn checkout(self) -> Checkout {
        Checkout {
            acct_num: self.acct_num,
            items: self.items,
        }
    }

    pub fn acct_num(&self) -> u32 {
        self.acct_num
    }

    pub fn tot_cost(&self) -> u32 {
        self.items.iter().sum()
    }
}

pub struct Checkout {
    acct_num: u32,
    items: Vec<u32>,
}

impl Checkout {
    pub fn cancel(self) -> NonEmpty {
        NonEmpty {
            acct_num: self.acct_num,
            items: self.items,
        }
    }

    pub fn order(self) -> Empty {
        Empty {
            acct_num: self.acct_num,
            tot_cost: 0,
        }
    }

    pub fn acct_num(&self) -> u32 {
        self.acct_num
    }

    pub fn tot_cost(&self) -> u32 {
        self.items.iter().sum()
    }
}

//===== END_CODE =====//
