/***************
 * NOTE:
 *   You can use `Sig`, `Pkt`, ..., `internal_send_pkts`
 *   which appear in the below `use` declarations,
 *   simply by `Sig`, `Pkt`, ..., `internal_send_pkts` without any prefixes.
 ***************/

#[allow(unused_imports)]
use crate::prob2::msg::{Pkt, Sig};
#[allow(unused_imports)]
use crate::prob2::server::{internal_send_pkts, internal_send_sig, Server};

// TODO: Implement the typestate structs below for the TCP client. You are free to add any fields
// that you think will be helpful to the struct definitions.
// Below shows the signature of the methods needed across the TCP client state machine.
// Note that not all methods may be implemented for every typestate struct.
//
//   pub fn new() -> T
//   pub fn send_syn(self, _: &mut Server) -> Result<T,T>
//   pub fn send_ack(self, _: &mut Server) -> T
//   pub fn send_pkts(self, _: &mut Server, _: &Vec<Pkt>) -> T
//   pub fn send_close(self, _: &mut Server) -> Result<T,T>
//   pub fn ids_sent(&self) -> Vec<u32>
//
// Here T denotes a type. Note that each T can be a different type.
//===== BEGIN_CODE =====//
pub struct Client {}

impl Client {
    pub fn new() -> Initial {
        Initial {}
    }
}

pub struct Initial {}

impl Initial {
    pub fn send_syn(self, server: &mut Server) -> Result<Syned, Initial> {
        match internal_send_sig(server, Sig::Syn) {
            Some(sig) => match sig {
                Sig::SynAck => Ok(Syned { ids_sent: vec![] }),
                _ => Err(self),
            },
            None => Err(self),
        }
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        vec![]
    }
}

pub struct Syned {
    ids_sent: Vec<u32>,
}

impl Syned {
    pub fn send_ack(self, server: &mut Server) -> SynAcked {
        internal_send_sig(server, Sig::Ack);
        SynAcked { ids_sent: vec![] }
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        self.ids_sent.clone()
    }
}

pub struct SynAcked {
    ids_sent: Vec<u32>,
}

impl SynAcked {
    pub fn send_pkts(mut self, server: &mut Server, pkts: &Vec<Pkt>) -> SynAcked {
        for pkt in pkts {
            let mut ok = internal_send_pkts(server, &vec![*pkt]);
            loop {
                if ok.contains(&pkt.id) {
                    self.ids_sent.push(pkt.id);
                    break;
                }
                ok = internal_send_pkts(server, &vec![*pkt]);
            }
        }
        self
    }

    pub fn send_close(self, server: &mut Server) -> Result<Closed, SynAcked> {
        let mut r = internal_send_sig(server, Sig::Close);
        loop {
            match r {
                Some(Sig::CloseAck) => {
                    return Ok(Closed {
                        ids_sent: self.ids_sent,
                    });
                }
                _ => {
                    r = internal_send_sig(server, Sig::Close);
                }
            }
        }
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        self.ids_sent.clone()
    }
}

pub struct Closed {
    ids_sent: Vec<u32>,
}

impl Closed {
    pub fn send_ack(self, server: &mut Server) -> Initial {
        internal_send_sig(server, Sig::Ack);
        Initial {}
    }

    pub fn ids_sent(&self) -> Vec<u32> {
        self.ids_sent.clone()
    }
}

//===== END_CODE =====//
