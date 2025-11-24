import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';
import { submitA1Form, getA1History } from '../../services/api';
import DateTimePicker from '../Common/DateTimePicker';
import FileUpload from '../Common/FileUpload';
import MultiSelect from '../Common/MultiSelect';
import GridSelector from '../Grid/GridSelector';
import HistoryTable from '../History/HistoryTable';
import DownloadButton from '../History/DownloadButton';
import './Form.css';

const A1Form = () => {
  const [formData, setFormData] = useState({
    date_time: '',
    lot_number: '',
    item_type: '',
    gsx_machine_no: '',
    mc_machine_no: '',
    cut_operator_payroll: '',
    ng_block_lot: '',
    ng_chip_qty_lot: '',
    block_number: '',
    confirm_date: '',
    reason: [],
    defects: [],
    judgement_block_a: 'Good',
    judgement_block_b: 'Good',
    judgement_block_c: 'Good',
    judgement_block_d: 'Good',
    shifting_amount_a: '',
    shifting_amount_b: '',
    shifting_amount_c: '',
    shifting_amount_d: '',
    shifting_direction_a: [],
    shifting_direction_b: [],
    shifting_direction_c: [],
    shifting_direction_d: [],
    quality_case: 'open',
    process_selection: [],
    grid: Array(6).fill(null).map(() => Array(6).fill(false))
  });

  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [errors, setErrors] = useState({});

  const reasonOptions = ['After Repair', 'After Shut Down', 'Change item', 'Others'];
  const defectOptions = [
    'w shift', 'L shift', 'Sheet NG', 'W out/ Lout', 'Deformed', 'Slant Cut', 
    'Pattern dent', 'Dragging', 'Smearing', 'Partial print', 'Blunt cut', 
    'Others', 'Rough cut', 'VP dent', 'Line', 'Step Shift', 'Ridge/Dent',
    'Cut Debris', 'Drop Chip', 'Electrode Horn', 'Blade Broken'
  ];
  const directionOptions = ['W shift front', 'W shift back', 'L shift right', 'L shift left', 'Sheet NG', 'good'];
  const processOptions = ['Stacking Feedback', 'Cutting Feedback'];

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await getA1History();
      setHistory(response.data);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const handleChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.date_time) newErrors.date_time = 'Required';
    if (!formData.lot_number || formData.lot_number.length > 10) {
      newErrors.lot_number = 'Required (max 10 characters)';
    }
    if (!formData.item_type) newErrors.item_type = 'Required';
    if (!formData.gsx_machine_no) newErrors.gsx_machine_no = 'Required';
    if (!formData.mc_machine_no) newErrors.mc_machine_no = 'Required';
    if (!formData.cut_operator_payroll) newErrors.cut_operator_payroll = 'Required';
    if (!formData.ng_block_lot) newErrors.ng_block_lot = 'Required';
    if (!formData.ng_chip_qty_lot) newErrors.ng_chip_qty_lot = 'Required';
    if (!formData.block_number) newErrors.block_number = 'Required';
    if (!formData.confirm_date) newErrors.confirm_date = 'Required';
    if (formData.reason.length === 0) newErrors.reason = 'Required';
    if (formData.defects.length === 0) newErrors.defects = 'Required';
    if (!formData.shifting_amount_a) newErrors.shifting_amount_a = 'Required';
    if (!formData.shifting_amount_b) newErrors.shifting_amount_b = 'Required';
    if (!formData.shifting_amount_c) newErrors.shifting_amount_c = 'Required';
    if (!formData.shifting_amount_d) newErrors.shifting_amount_d = 'Required';
    if (formData.shifting_direction_a.length === 0) newErrors.shifting_direction_a = 'Required';
    if (formData.shifting_direction_b.length === 0) newErrors.shifting_direction_b = 'Required';
    if (formData.shifting_direction_c.length === 0) newErrors.shifting_direction_c = 'Required';
    if (formData.shifting_direction_d.length === 0) newErrors.shifting_direction_d = 'Required';
    if (formData.process_selection.length === 0) newErrors.process_selection = 'Required';
    if (files.length === 0) newErrors.files = 'At least one photo is required';

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      toast.error('Please fill all required fields');
      return;
    }

    setLoading(true);
    try {
      const formDataToSend = new FormData();
      
      // Add all form fields
      Object.keys(formData).forEach(key => {
        if (key === 'grid') {
          formDataToSend.append(key, JSON.stringify(formData[key]));
        } else if (Array.isArray(formData[key])) {
          formDataToSend.append(key, JSON.stringify(formData[key]));
        } else {
          formDataToSend.append(key, formData[key]);
        }
      });

      // Add files
      files.forEach(file => {
        formDataToSend.append('photos', file);
      });

      await submitA1Form(formDataToSend);
      toast.success('Form submitted successfully!');
      
      // Reset form
      handleClear();
      loadHistory();
    } catch (error) {
      toast.error(error.message || 'Failed to submit form');
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFormData({
      date_time: '',
      lot_number: '',
      item_type: '',
      gsx_machine_no: '',
      mc_machine_no: '',
      cut_operator_payroll: '',
      ng_block_lot: '',
      ng_chip_qty_lot: '',
      block_number: '',
      confirm_date: '',
      reason: [],
      defects: [],
      judgement_block_a: 'Good',
      judgement_block_b: 'Good',
      judgement_block_c: 'Good',
      judgement_block_d: 'Good',
      shifting_amount_a: '',
      shifting_amount_b: '',
      shifting_amount_c: '',
      shifting_amount_d: '',
      shifting_direction_a: [],
      shifting_direction_b: [],
      shifting_direction_c: [],
      shifting_direction_d: [],
      quality_case: 'open',
      process_selection: [],
      grid: Array(6).fill(null).map(() => Array(6).fill(false))
    });
    setFiles([]);
    setErrors({});
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit}>
        <div className="form-section">
          <h2 className="form-title">A1 Cutting Process Feedback</h2>
          
          <div className="form-row">
            <div className="form-group">
              <DateTimePicker
                label="Date and Time"
                value={formData.date_time}
                onChange={(value) => handleChange('date_time', value)}
                error={errors.date_time}
              />
            </div>
            <div className="form-group">
              <label>Lot Number (max 10 chars)</label>
              <input
                type="text"
                value={formData.lot_number}
                onChange={(e) => handleChange('lot_number', e.target.value)}
                maxLength={10}
                className={errors.lot_number ? 'error' : ''}
              />
              {errors.lot_number && <div className="error-message">{errors.lot_number}</div>}
            </div>
            <div className="form-group">
              <label>Item Type</label>
              <input
                type="text"
                value={formData.item_type}
                onChange={(e) => handleChange('item_type', e.target.value)}
                className={errors.item_type ? 'error' : ''}
              />
              {errors.item_type && <div className="error-message">{errors.item_type}</div>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>GSX Machine No</label>
              <input
                type="text"
                value={formData.gsx_machine_no}
                onChange={(e) => handleChange('gsx_machine_no', e.target.value)}
                className={errors.gsx_machine_no ? 'error' : ''}
              />
              {errors.gsx_machine_no && <div className="error-message">{errors.gsx_machine_no}</div>}
            </div>
            <div className="form-group">
              <label>MC Machine No</label>
              <input
                type="text"
                value={formData.mc_machine_no}
                onChange={(e) => handleChange('mc_machine_no', e.target.value)}
                className={errors.mc_machine_no ? 'error' : ''}
              />
              {errors.mc_machine_no && <div className="error-message">{errors.mc_machine_no}</div>}
            </div>
            <div className="form-group">
              <label>Cut Operator Payroll</label>
              <input
                type="text"
                value={formData.cut_operator_payroll}
                onChange={(e) => handleChange('cut_operator_payroll', e.target.value)}
                className={errors.cut_operator_payroll ? 'error' : ''}
              />
              {errors.cut_operator_payroll && <div className="error-message">{errors.cut_operator_payroll}</div>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>NG Block/Lot</label>
              <input
                type="text"
                value={formData.ng_block_lot}
                onChange={(e) => handleChange('ng_block_lot', e.target.value)}
                className={errors.ng_block_lot ? 'error' : ''}
              />
              {errors.ng_block_lot && <div className="error-message">{errors.ng_block_lot}</div>}
            </div>
            <div className="form-group">
              <label>NG chip Qty/Lot(pcs)</label>
              <input
                type="text"
                value={formData.ng_chip_qty_lot}
                onChange={(e) => handleChange('ng_chip_qty_lot', e.target.value)}
                className={errors.ng_chip_qty_lot ? 'error' : ''}
              />
              {errors.ng_chip_qty_lot && <div className="error-message">{errors.ng_chip_qty_lot}</div>}
            </div>
            <div className="form-group">
              <label>Block Number</label>
              <input
                type="text"
                value={formData.block_number}
                onChange={(e) => handleChange('block_number', e.target.value)}
                className={errors.block_number ? 'error' : ''}
              />
              {errors.block_number && <div className="error-message">{errors.block_number}</div>}
            </div>
            <div className="form-group">
              <label>Confirm Date</label>
              <input
                type="date"
                value={formData.confirm_date}
                onChange={(e) => handleChange('confirm_date', e.target.value)}
                className={errors.confirm_date ? 'error' : ''}
              />
              {errors.confirm_date && <div className="error-message">{errors.confirm_date}</div>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <MultiSelect
                label="Reason"
                options={reasonOptions}
                value={formData.reason}
                onChange={(value) => handleChange('reason', value)}
                error={errors.reason}
              />
            </div>
            <div className="form-group">
              <MultiSelect
                label="Defect Name"
                options={defectOptions}
                value={formData.defects}
                onChange={(value) => handleChange('defects', value)}
                error={errors.defects}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Judgement Block A</label>
              <select
                value={formData.judgement_block_a}
                onChange={(e) => handleChange('judgement_block_a', e.target.value)}
                style={{ color: formData.judgement_block_a === 'Good' ? 'green' : 'red' }}
              >
                <option value="Good">Good</option>
                <option value="NG">NG</option>
              </select>
            </div>
            <div className="form-group">
              <label>Judgement Block B</label>
              <select
                value={formData.judgement_block_b}
                onChange={(e) => handleChange('judgement_block_b', e.target.value)}
                style={{ color: formData.judgement_block_b === 'Good' ? 'green' : 'red' }}
              >
                <option value="Good">Good</option>
                <option value="NG">NG</option>
              </select>
            </div>
            <div className="form-group">
              <label>Judgement Block C</label>
              <select
                value={formData.judgement_block_c}
                onChange={(e) => handleChange('judgement_block_c', e.target.value)}
                style={{ color: formData.judgement_block_c === 'Good' ? 'green' : 'red' }}
              >
                <option value="Good">Good</option>
                <option value="NG">NG</option>
              </select>
            </div>
            <div className="form-group">
              <label>Judgement Block D</label>
              <select
                value={formData.judgement_block_d}
                onChange={(e) => handleChange('judgement_block_d', e.target.value)}
                style={{ color: formData.judgement_block_d === 'Good' ? 'green' : 'red' }}
              >
                <option value="Good">Good</option>
                <option value="NG">NG</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Shifting Amount A (micron)</label>
              <input
                type="text"
                value={formData.shifting_amount_a}
                onChange={(e) => handleChange('shifting_amount_a', e.target.value)}
                className={errors.shifting_amount_a ? 'error' : ''}
              />
              {errors.shifting_amount_a && <div className="error-message">{errors.shifting_amount_a}</div>}
            </div>
            <div className="form-group">
              <label>Shifting Amount B (micron)</label>
              <input
                type="text"
                value={formData.shifting_amount_b}
                onChange={(e) => handleChange('shifting_amount_b', e.target.value)}
                className={errors.shifting_amount_b ? 'error' : ''}
              />
              {errors.shifting_amount_b && <div className="error-message">{errors.shifting_amount_b}</div>}
            </div>
            <div className="form-group">
              <label>Shifting Amount C (micron)</label>
              <input
                type="text"
                value={formData.shifting_amount_c}
                onChange={(e) => handleChange('shifting_amount_c', e.target.value)}
                className={errors.shifting_amount_c ? 'error' : ''}
              />
              {errors.shifting_amount_c && <div className="error-message">{errors.shifting_amount_c}</div>}
            </div>
            <div className="form-group">
              <label>Shifting Amount D (micron)</label>
              <input
                type="text"
                value={formData.shifting_amount_d}
                onChange={(e) => handleChange('shifting_amount_d', e.target.value)}
                className={errors.shifting_amount_d ? 'error' : ''}
              />
              {errors.shifting_amount_d && <div className="error-message">{errors.shifting_amount_d}</div>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <MultiSelect
                label="Shifting Direction A"
                options={directionOptions}
                value={formData.shifting_direction_a}
                onChange={(value) => handleChange('shifting_direction_a', value)}
                error={errors.shifting_direction_a}
              />
            </div>
            <div className="form-group">
              <MultiSelect
                label="Shifting Direction B"
                options={directionOptions}
                value={formData.shifting_direction_b}
                onChange={(value) => handleChange('shifting_direction_b', value)}
                error={errors.shifting_direction_b}
              />
            </div>
            <div className="form-group">
              <MultiSelect
                label="Shifting Direction C"
                options={directionOptions}
                value={formData.shifting_direction_c}
                onChange={(value) => handleChange('shifting_direction_c', value)}
                error={errors.shifting_direction_c}
              />
            </div>
            <div className="form-group">
              <MultiSelect
                label="Shifting Direction D"
                options={directionOptions}
                value={formData.shifting_direction_d}
                onChange={(value) => handleChange('shifting_direction_d', value)}
                error={errors.shifting_direction_d}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Quality Case</label>
              <select
                value={formData.quality_case}
                onChange={(e) => handleChange('quality_case', e.target.value)}
              >
                <option value="open">open</option>
                <option value="close">close</option>
              </select>
            </div>
            <div className="form-group">
              <MultiSelect
                label="Process Selection"
                options={processOptions}
                value={formData.process_selection}
                onChange={(value) => handleChange('process_selection', value)}
                error={errors.process_selection}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <GridSelector
                size={6}
                value={formData.grid}
                onChange={(grid) => handleChange('grid', grid)}
                showBlockLabels={true}
                label="GSX MACHINE BACKSIDE / FRONT SIDE"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <FileUpload
                files={files}
                onChange={setFiles}
                error={errors.files}
              />
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn-secondary" onClick={handleClear}>
              Clear
            </button>
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? (
                <>
                  <span className="loading-spinner"></span>
                  Submitting...
                </>
              ) : (
                'Send Email'
              )}
            </button>
          </div>
        </div>
      </form>

      <div className="form-section">
        <h2 className="form-title">Summary History</h2>
        <HistoryTable data={history} />
        <DownloadButton formType="a1" />
      </div>
    </div>
  );
};

export default A1Form;


