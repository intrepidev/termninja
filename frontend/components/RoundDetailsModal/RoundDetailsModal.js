import React, { useState, useEffect } from 'react';
import { Modal,
         ModalBody } from 'reactstrap';
import api from '../../api';
import RoundModalHeader from './RoundModalHeader';
import classes from './RoundDetailsModal.css';


const emptyRound = {
  'server_name': '',
  'result_snapshot': '',
  'result_message': '',
  'user_username': '',
  'gravatar_hash': '',
  'score': 0,
}

const RoundDetailsModal = ({ roundId, onClose }) => {
  const [round, setRound] = useState(emptyRound);
  const [loading, setLoading] = useState(false);

  console.log(round);

  useEffect(() => {
    const updateRound = async () => {
      setLoading(true);
      let round = emptyRound;
      if (roundId) {
        round = await api.round.getDetails(roundId);
      }
      setLoading(false);
      setRound(round)
    }
    updateRound();
  }, [roundId])

  return (
    <Modal isOpen={Boolean(roundId)} className={classes.root}>
      <ModalBody>
        <RoundModalHeader { ...round } onClose={onClose} />
        <span className={`${classes.message} m-2`}>{ round.message }</span>
        { round.snapshot &&
          <pre className={`${classes.snapshot} py-3 pr-2 font-weight-bold mt-3 text-center`} 
               dangerouslySetInnerHTML={{ __html: round.snapshot }} />
        }
      </ModalBody>

    </Modal>
  )
}

export default RoundDetailsModal;